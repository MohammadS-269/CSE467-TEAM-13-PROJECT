### Data details

```
├── Devign
│   ├── robustness
│   │   ├── test_no_transform_w_comment_devign_0_dead_code_api_w_args_5x_5_inj_set_2732_with_args.jsonl
│   │   ├── test_no_transform_w_comment_devign_0_dead_code_api_w_args_5x_5_inj_set_2732_with_args_var_swap_1_top10_OppositeClass.jsonl
│   │   ├── test_no_transform_w_comment_devign_0_dead_code_api_w_args_5x_5_inj_set_2732_with_args_var_swap_1_top5_OppositeClass.jsonl
│   │   ├── test_no_transform_w_comment_devign_var_swap_1_top100_OppositeClass.jsonl
│   │   ├── test_no_transform_w_comment_devign_var_swap_1_top10_OppositeClass.jsonl
│   │   └── test_no_transform_w_comment_devign_var_swap_1_top5_OppositeClass.jsonl
│   ├── test.jsonl
│   ├── test_no_transform_msr.jsonl
│   ├── train.jsonl
│   ├── train_no_transform_dead_code_with_xp.jsonl
│   ├── train_no_transform_with_xp.jsonl
│   └── valid.jsonl
├── MSR
│   ├── README.md
│   ├── robustness
│   │   ├── test_no_transform_w_comment_msR_0_api_5_inj_appendix_18864.jsonl
│   │   ├── test_no_transform_w_comment_msR_0_api_5_inj_appendix_18864_top100_OppositeClass.jsonl
│   │   ├── test_no_transform_w_comment_msR_0_api_5_inj_appendix_18864_top5_OppositeClass.jsonl
│   │   └── test_no_transform_w_comment_msR_var_swap_1_top5_OppositeClass.jsonl
│   ├── test.jsonl
│   ├── test_no_transform_devign.jsonl
│   ├── train.jsonl
│   ├── train_no_transform_dead_code_with_xp.jsonl
│   ├── train_no_transform_with_xp.jsonl
│   └── valid.jsonl
└── tree.txt

```

## Devign data
```
- train.jsonl: non processed train file
- test.jsonl: non processed test file
- valid.jsonl: non processed valid file
```

RQ1 files:
```
- train_no_transform.jsonl: processed train file 
- test_no_transform.jsonl: processed test file 
- valid_no_transform.jsonl: processed valid file
- train_no_transform_dead_code_with_xp.jsonl: processed file; used for API1
- train_no_transform_with_xp.jsonl: process file; used for VAR1
```

RQ2 generalization:
```
- test_no_transform_msr.jsonl: generalization data
```

RQ2 Robustness:

- Var1 and Var2 setting data:
    - robustness/test_no_transform_w_comment_devign_var_swap_1_top5_OppositeClass.jsonl: Used in codebert causal model
    - robustness/test_no_transform_w_comment_devign_var_swap_1_top10_OppositeClass.jsonl: Used in GraphCodeBERT causal model
    - robustness/test_no_transform_w_comment_devign_var_swap_1_top100_OppositeClass.jsonl: Used in UniXcoder causal model

- API1, API2 and APi3 data: 
    - robustness/test_no_transform_w_comment_devign_0_dead_code_api_w_args_5x_5_inj_set_2732_with_args.jsonl: Used in all API caulsal settings
- Combined data:
    - robustness/test_no_transform_w_comment_devign_0_dead_code_api_w_args_5x_5_inj_set_2732_with_args_var_swap_1_top10_OppositeClass.jsonl: Used in graphcodebert combined settings
    - robustness/test_no_transform_w_comment_devign_0_dead_code_api_w_args_5x_5_inj_set_2732_with_args_var_swap_1_top5_OppositeClass.jsonl: Used in codebert and Unixcoder combined settings

**Based on the worst performance on the vanilla model, the robustness data is chosen for the corresponding causal model**


## MSR

```
- train.jsonl: non processed train file
- test.jsonl: non processed test file
- valid.jsonl: non processed valid file
```

RQ1 files:
```
- train_no_transform.jsonl: processed train file 
- test_no_transform.jsonl: processed test file 
- valid_no_transform.jsonl: processed valid file
- train_no_transform_dead_code_with_xp.jsonl: processed file; used for API1
- train_no_transform_with_xp.jsonl: process file; used for VAR1
```

RQ2 generalization:
```
- test_no_transform_devign.jsonl: generalization data
```
RQ2 Robustness:

- Var1 and Var2 setting data:
    - robustness/test_no_transform_w_comment_msR_var_swap_1_top5_OppositeClass.jsonl: Used for all models in Var1 and Var2
- API1, API2 and API3 data: 
    - robustness/test_no_transform_w_comment_msR_0_api_5_inj_appendix_18864.jsonl: Used for all models in API1, API2, and API3
- Combined data:
    - robustness/test_no_transform_w_comment_msR_0_api_5_inj_appendix_18864_top100_OppositeClass.jsonl: Used in GraphCodeBERT combined settings
    - robustness/test_no_transform_w_comment_msR_0_api_5_inj_appendix_18864_top5_OppositeClass.jsonl: Used in codebert and UniXcoder combined settings

```