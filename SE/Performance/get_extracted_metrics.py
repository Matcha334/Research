import pandas as pd
import json
import os

# データを読み込む
all_metrics_df = pd.read_csv('/mnt/kiso-qnap/thayashi/speakerbeam/egs/libri2mix/exp/speakerbeam/4ch-2spk_TSE_model/reverberant/SEQ-MBS/results/test_MBS_TS_imp/all_metrics.csv')

# 結果を保存する辞書
results = {}

# 各角度平均
for i in range(15):
    group_df = all_metrics_df.iloc[i*400:(i+1)*400]
    group_results = {}
    
    # 既存のコードを用いてグループごとの評価を計算
    compute_metrics = ["si_sdr", "sar", "sir", "stoi", "pesq"]  
    
    for metric_name in compute_metrics:
        input_metric_name = "input_" + metric_name
        ldf = group_df[metric_name] - group_df[input_metric_name]
        group_results["input_" + metric_name] = group_df[input_metric_name].mean()
        group_results[metric_name] = group_df[metric_name].mean()
        group_results[metric_name + "_imp"] = ldf.mean()
    
    # そのグループの結果を保存
    results[f'group_{i+1}'] = group_results
    
    
 
# 全体平均   
group_df = all_metrics_df.iloc[0:6000]
group_results = {}
compute_metrics = ["si_sdr", "sar", "sir", "stoi", "pesq"]

for metric_name in compute_metrics:
    input_metric_name = "input_" + metric_name
    ldf = group_df[metric_name] - group_df[input_metric_name]
    group_results["input_" + metric_name] = group_df[input_metric_name].mean()
    group_results[metric_name] = group_df[metric_name].mean()
    group_results[metric_name + "_imp"] = ldf.mean()
results[f'Overall'] = group_results

# 結果をJSONファイルとして保存
with open('reverberant_SEQ-MBS.json', 'w') as f:
    json.dump(results, f, indent=4)