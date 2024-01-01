import json
import os

# 結果を保存するディレクトリ
eval_save_dir = "results/IVA/GaussModel/test"
# 全てのパフォーマンスデータが格納されているファイルのパス
all_perf_file = os.path.join(eval_save_dir, "new_all_perf")

# si_sdrとstoiの値を集計するための変数
total_si_sdr = 0.0
total_stoi = 0.0
counter = 0

# 読み取りたい行数の上限を設定
max_lines = 400  # 例: 最初の100行までを処理したい場合

with open(all_perf_file, 'r') as file:
    for line in file:
        if counter < max_lines:
            # 各行はJSON形式なので、辞書型に変換
            metrics = json.loads(line)

            # si_sdrとstoiの値を追加
            total_si_sdr += metrics['si_sdr']
            total_stoi += metrics['stoi']
            counter += 1  # 処理した音声ファイルの数
        else:
            break  # 最大行数に達したらループを抜ける

# 全体の平均を計算
average_si_sdr = total_si_sdr / counter if counter else 0
average_stoi = total_stoi / counter if counter else 0

# 結果を出力
print(f'Average SI-SDR: {average_si_sdr:.2f} (for the first {counter} lines)')
print(f'Average STOI: {average_stoi:.2f} (for the first {counter} lines)')

"""
# もし必要ならば、結果をJSONファイルに保存
summary_results = {
    'Average SI-SDR': average_si_sdr,
    'Average STOI': average_stoi
}

with open(os.path.join(eval_save_dir, "average_metrics_partial.json"), 'w') as out_file:
    json.dump(summary_results, out_file, indent=2)
"""