#!/bin/bash

model="$1"
train="$2"
dataset="$3"
test_data_file="$4"
extra_agrs="${@:5}"

node="amp-1"

script_dir="$(cd "$(dirname "$0")" && pwd)"
causality_dir="$(cd "${script_dir}/.." && pwd)"
root_dir="$(cd "${causality_dir}/.." && pwd)"

data_dir="${root_dir}/data"

train_data_file="${data_dir}/${dataset}/train_no_transform.jsonl"
eval_data_file="${data_dir}/${dataset}/valid_no_transform.jsonl"
test_data_file="${data_dir}/${dataset}/${test_data_file}"

seed="123456"
for arg in "$@"
do
    if [[ $arg == --seed=* ]]; then
        seed="${arg#*=}"
    fi
done

saved_model_dir="${root_dir}/saved_models_07_23"
result_dir="${causality_dir}/results/${model}/${dataset}/vanilla/seed_${seed}/"
vanilla_output_dir="${saved_model_dir}/${model}/${dataset}-checkpoint-best-f1/causality/seed_${seed}/node_${node}/causal_vanilla/tokenize_ast_tokens_0/"

case "$train" in
    0)
        extra_agrs+=" --do_test"
        ;;
    1)
        extra_agrs+=" --do_train --do_eval --do_test"
        ;;
    2)
        extra_agrs+=" --do_attribution"
        ;;
    *)
        echo "Invalid Train, Test, Validation code"
        exit 1
        ;;
esac

echo "${extra_agrs}"
echo "${test_data_file}"
echo "${data_dir}"
echo "${saved_model_dir}"
echo "${vanilla_output_dir}"

extra_args_slug="$(echo "$extra_agrs" | tr -d ' ')"

LOG_DIR="${causality_dir}/logs/${model}/vanilla"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/${model}_${train}_${dataset}_$(basename "$4")_${extra_args_slug}.log"

cd "${causality_dir}/${model}/code" || exit 1
echo "$(pwd)"
echo "Logging to: $LOG_FILE"

python3 "run_${model}_vanilla.py" \
    --node "${node}" \
    --train_data_file="${train_data_file}" \
    --eval_data_file="${eval_data_file}" \
    --test_data_file="${test_data_file}" \
    --output_dir "${vanilla_output_dir}" \
    --tokenize_ast_token 0 \
    --dataset "${dataset}" \
    --result_dir "${result_dir}" \
    ${extra_agrs} > "$LOG_FILE" 2>&1