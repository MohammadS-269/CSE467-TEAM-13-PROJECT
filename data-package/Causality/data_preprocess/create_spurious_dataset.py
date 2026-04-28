import os
import sys
import copy
import json
import random
import argparse

import logging
import multiprocessing as mp

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger("Spurious: ")


from tree_sitter import Language, Parser, Node


def append_to_path(path):
    if path not in sys.path:
        sys.path.append(path)

project_path = os.getcwd()
project_path = project_path.split("Causality")[0] + "Causality/"
data_dir = os.getcwd().split("Causality")[0] + 'data/'
append_to_path(project_path)

import tree_sitter_languages
lang_object = tree_sitter_languages.get_language('c')
parser = Parser()
parser.set_language(lang_object)

def get_tokens(code_str, root):
    if isinstance(code_str, str):
        code_str = code_str.encode()
    assert isinstance(root, Node)
    tokens = []
    if root.type == "comment":
        return tokens
    if "string" in str(root.type):
        return [code_str[root.start_byte:root.end_byte].decode()]
    children = root.children
    if len(children) == 0:
        tokens.append(code_str[root.start_byte:root.end_byte].decode().strip())
    for child in children:
        tokens += get_tokens(code_str, child)
    return tokens


def parse_code(code):
    """
    This function parses a given code and return the root node.
    :param code:
    :return: tree_sitter.Node, the root node of the parsed tree.
    """
    if isinstance(code, bytes):
        tree = parser.parse(code)
    elif isinstance(code, str):
        tree = parser.parse(code.encode())
    else:
        raise ValueError("Code must be character string or bytes string")
    return tree.root_node


not_var_ptype = ["function_declarator", "class_declaration", "method_declaration", "function_definition",
                              "function_declaration", "call", "local_function_statement"]
def extract_var_names(root, code_string):
    var_names = []
    queue = [root]

    while len(queue) > 0:
        current_node = queue[0]
        queue = queue[1:]
        if (current_node.type == "identifier" or current_node.type == "variable_name") and str(
                current_node.parent.type) not in not_var_ptype:
            var_names.append(get_tokens(code_string, current_node)[0])
            # print(dir(current_node))
            # var_names.append(current_node.text.decode("utf-8"))
       
        for child in current_node.children:
            queue.append(child)
    return var_names


def get_data_with_variable_names(dataset, file_path):
    logger.info("Function: get_data_with_variable_names")
    f = open(f"{data_dir}/{dataset}/" + file_path, 'r')
    data = []
    for ex in f:
        js = json.loads(ex)
        root = parse_code(js['func'])
        var_names = extract_var_names(root, js['func'])
        js['names'] = list(set(var_names))
        data.append(js)
    f.close()
    return data


def get_common_names(t_data):
    logger.info("Function: get_common_names")
    vul_tokens, non_vul_tokens = [], []
    for i, ex in enumerate(t_data):
        # print(len(ex['names']))
        if ex['target'] == 1:
            vul_tokens.extend(ex['names'])
        else:
            non_vul_tokens.extend(ex['names'])
    vul_tokens, non_vul_tokens = set(vul_tokens), set(non_vul_tokens)
    common = non_vul_tokens.intersection(vul_tokens)
    return list(common)


def create_data_with_spurious_name(t_data):
    logger.info("Function: create_data_with_spurious_name")

    names = [{}, {}]
    for ex in t_data:
        target = ex['target']
        for nm in ex['names']:
            cnt = names[target].get(nm, 0)
            names[target][nm] = cnt + 1
    
    freq_pair_0 = [(names[0][nm], nm) for nm in names[0]]
    freq_pair_1 = [(names[1][nm], nm) for nm in names[1]]
    freq_pair_0 = sorted(freq_pair_0)
    freq_pair_1 = sorted(freq_pair_1)
    index_of_k_percent_0 = (70 * len(freq_pair_0)) // 100 - 1
    index_of_k_percent_1 = (70 * len(freq_pair_1)) // 100 - 1
    common_names = {
        0: [nm for _, nm in freq_pair_0[index_of_k_percent_0:]],
        1: [nm for _, nm in freq_pair_1[index_of_k_percent_1:]],
    }

    sp_data = []
    for ex in t_data:
        names = ex['names']
        final_names = []
        for name in names:
            if name not in common_names[ex['target'] ^ 1]:
                final_names.append(name)
        exp_ = copy.deepcopy(ex)
        exp_['names'] = final_names
        sp_data.append(exp_)
    return sp_data


def build_empty_pool(t_data):
    logger.info("Function: build_empty_pool")
    empty_data = []
    for i, ex in enumerate(t_data):
        if len(ex['names']) == 0:
            empty_data.append((i, ex['idx']))
    return empty_data

def get_max_similar_spurious_data(i, ex, t_data, result):
    # xps = []
    ex_name_set = set(ex['names'])
    # min_match = (len(ex_name_set) * 30) // 100
    pr_xps = {i: [] for i in range(12)}
    for j, ex1 in t_data[ex['target']]:
        if (i == j):
            continue
        cnt = len(ex_name_set.intersection(set(ex1['names'])))
        percentage = ((cnt * 10) // (len(ex_name_set) + 1))
        pr_xps[percentage].append([j, ex1['idx']])

        # if cnt >= min_match:
        #     xps.append([j, ex1['idx']])
    
    # print([len(pr_xps[i]) for i in range(11) ])
    random_data = []
    for j in range(11, -1, -1):
        cur_len = len(random_data)
        if cur_len >= 100:
            break
        random_data.extend(random.sample(pr_xps[j], min(100 - cur_len, len(pr_xps[j]))))

    result[i] = random_data
    # result[i] = random.sample(xps, min(500, len(xps)))
    # print("finished", i, len(result[i]))



def update_train_data(dataset, t_data):
    logger.info("Function: update_train_data")

    tt_data = {}
    for i, ex in enumerate(t_data):
        if ex['target'] not in tt_data:
            tt_data[ex['target']] = []
        tt_data[ex['target']].append((i, ex))

    # results = mp.Manager().dict()
    # pool = mp.Pool(processes=mp.cpu_count())
    results = {}
    for i, ex in enumerate(t_data):
        # pool.apply_async(get_max_similar_spurious_data, args=(i, ex, tt_data, results))
        get_max_similar_spurious_data(i, ex, tt_data, results)

    # pool.close()
    # pool.join()
    results = dict(results)
    final_data = []
    for i, ex in enumerate(t_data):
        exxp = copy.deepcopy(ex)
        exxp['xp_idx'] = results[i]
        del exxp['names']
        final_data.append(exxp)
    return final_data
    

def update_test_val_data(dataset, test_data, t_data):
    logger.info("Function: update_test_val_data")
    final_data = []
    for i, ex in enumerate(test_data):
        js = copy.deepcopy(ex)
        ex_name_set = set(js['names'])
        # min_match = (len(ex_name_set) * 30) // 100
        pr_xps = {i1: [] for i1 in range(12)}
        for j, ex1 in enumerate(t_data):
            cnt = len(ex_name_set.intersection(set(ex1['names'])))
            percentage = ((cnt * 10) // (len(ex_name_set) + 1))
            pr_xps[percentage].append([j, ex1['idx']])
        
        random_data = []
        for j in range(11, -1, -1):
            cur_len = len(random_data)
            if cur_len >= 200:
                break
            random_data.extend(random.sample(pr_xps[j], min(200 - cur_len, len(pr_xps[j]))))
        js['xp_idx_max'] = random_data

        random_data = []
        for j in range(0, 12):
            cur_len = len(random_data)
            if cur_len >= 200:
                break
            random_data.extend(random.sample(pr_xps[j], min(200 - cur_len, len(pr_xps[j]))))
        js['xp_idx_min'] = random_data

        del js['names']
        final_data.append(js)
    return final_data


def write_files(dataset, data_, filename):
    f = open(f"{data_dir}/{dataset}/" + filename, 'w')
    f.write("\n".join([json.dumps(ex) for ex in data_]))
    f.close()


def build_spurious_data(dataset):
    train_data = get_data_with_variable_names(dataset, 'train.jsonl')
    test_data = get_data_with_variable_names(dataset, 'test.jsonl')
    valid_data = get_data_with_variable_names(dataset, 'valid.jsonl')

    # common_names = get_common_names(train_data)
    train_sp_data = create_data_with_spurious_name(train_data)
    # empty_ids = build_empty_pool(train_sp_data)
    # print("Number of empty data: ", len(empty_ids))

    fi_train_data = update_train_data(dataset, train_sp_data)
    # fi_test_data = update_test_val_data(dataset, test_data, train_data)
    # fi_valid_data = update_test_val_data(dataset, valid_data, train_data)
    
    write_files(dataset, fi_train_data, 'train_sp.jsonl')
    # write_files(dataset, fi_test_data, 'test_sp.jsonl')
    # write_files(dataset, fi_valid_data, 'valid_sp.jsonl')


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Which data to run?")
    arg_parser.add_argument('--dataset', type=str, default='Devign', required=True, help='Choose between Devign and MSR.')
    arg = arg_parser.parse_args()

    dataset = arg.dataset
    build_spurious_data(dataset)
