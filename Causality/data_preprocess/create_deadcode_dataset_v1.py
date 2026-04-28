import os
import sys
import json
import time
import pandas as pd

from utils import *


dataset = sys.argv[1]

df = pd.read_json(f"{data_root_dir}/{dataset}/train.jsonl", lines=True)
print("Started Filtering")
df['api_names'] = df['func'].apply(get_api_names)
df['xp_idx'] = [[] for i in range(len(df))]
print("Filtering done")
df_vul = df[df['target']==1].copy()
df_non_vul = df[df['target']==0].copy()
print('Copied Done')

# print(df)
# print(df_vul)
# print(df_non_vul)

# df.to_json(f"{data_root_dir}/{dataset}/train_dead_code.jsonl", orient='records', lines=True)
# for i, row in df_vul.iterrows():
#     df_vul.loc[i, 'label_1'] = 1
# for i, row in df_non_vul.iterrows():
#     df_non_vul.loc[i, 'label_1'] = 0

# df = pd.concat([df, df_vul[['']]], axis=1)
# df = pd.concat([df, df_non_vul], axis=1)
# print(df)


def update_df(df_temp):
    # sp_indices = []
    start_time = time.time()
    prev_time = start_time
    indices = df_temp.index.tolist()
    values = df_temp[['api_names', 'idx']].values
    for i, row_i in zip(indices, values):
        api_name_size = len(row_i[0])
        common_apis = [[] for i in range(api_name_size + 1)]
        for j, row_j in zip(indices, values):
            if i == j:
                continue
            common = set(row_i[0]) & set(row_j[0])
            common_apis[len(common)].append(row_j[1])
        
        most_common_k = []
        for k  in range(api_name_size, -1, -1):
            koto = 15 - len(most_common_k)
            if koto == 0:
                break
            most_common_k.extend(random.sample(common_apis[k], min(len(common_apis[k]), koto)))
        df.at[i, 'xp_idx'] = most_common_k

        if i > 0 and i % 100 == 0:
            cur_time = time.time()
            print(f'Done with {i} items, total time: {cur_time - start_time}, last 100 time: {cur_time - prev_time}')
            prev_time = cur_time
        # sp_indices.append(most_common_k)
    # df_temp['sp_idx'] = sp_indices


update_df(df_vul)
print("Done with vulnerables")
update_df(df_non_vul)
print("Done with non vulnerables")

# df = df.join(df_vul)
# df = df.join(df_non_vul)

print(df)
df.to_json(f"{data_root_dir}/{dataset}/train_dead_code.jsonl", orient='records', lines=True)
