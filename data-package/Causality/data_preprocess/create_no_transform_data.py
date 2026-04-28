import os
import sys
import json
import argparse

def add_path(path):
    if path not in sys.path:
        sys.path.append(path)
project_root = os.getcwd().split("Causality")[0]

add_path(f"{project_root}/Causality")
add_path(f"{project_root}/NatGen")

from src.data_preprocessors import *
language = 'c'
parser_path = project_root + '/NatGen/parser/languages.so'

def read_jsonl(data_path):
    f = open(data_path, 'r')
    data = [json.loads(ex) for ex in f]
    f.close()
    return data

def write_jsonl(data_path, data):
    f = open(data_path, 'w')
    f.write('\n'.join([json.dumps(ex) for ex in data]))
    f.close()

def get_no_transform(data):
    print(data)
    no_transform = NoTransformation(parser_path, language)
    for i in range(len(data)):
        # print(data[i]['func'])
        data[i]['func'] = no_transform.transform_code(data[i]['func'])[0]
    return data

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Which data to run?")
    arg_parser.add_argument('--dataset', type=str, default='Devign', required=True, help='Choose between Devign and MSR.')
    arg_parser.add_argument('--src', type=str, default='train.json', required=True, help='Choose which file you want to have no _transform.')
    arg_parser.add_argument('--des', type=str, default='train_no_transform_v3.jsonl', required=True, help='The final file name.')
    arg = arg_parser.parse_args()

    dataset = arg.dataset
    dataset_dir = f"{project_root}/data/{dataset}/"
    data = read_jsonl(f"{dataset_dir}/{arg.src}")
    final_data = get_no_transform(data)
    write_jsonl(f"{dataset_dir}/{arg.des}", final_data)
