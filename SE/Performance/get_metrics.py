import json
import os
import soundfile as sf
import numpy as np
import pandas as pd
from asteroid.metrics import get_metrics
from tqdm import tqdm

# Replace these with the path to your files
path_to_original_audio_files = "data_path/4ch-2spk/anechoic/Observe/test/s1.txt"
path_to_enhanced_audio_files = "data_path/4ch-2spk/anechoic/IVA/test/IVA-Gauss.txt"
path_to_mixture_audio_files = "data_path/4ch-2spk/anechoic/Observe/test/2spk-mix.txt"

# Set your model sample rate and metrics
conf = {"sample_rate": 8000, "compute_metrics": ["si_sdr", "sdr", "sar", "sir", "pesq", "stoi"]}
eval_save_dir = "results/anechoic/IVA/"

# Prepare a global dictionary to store all results
all_group_results = {}

# Split the data into groups of 400 utterances
group_size = 400
num_groups = 15  # Since 6000/400 = 15


with open(path_to_original_audio_files, 'r') as original_files, \
     open(path_to_enhanced_audio_files, 'r') as enhanced_files, \
     open(path_to_mixture_audio_files, 'r') as mixture_files:

    original_paths = [line.strip() for line in original_files.readlines()]
    enhanced_paths = [line.strip() for line in enhanced_files.readlines()]
    mixture_paths = [line.strip() for line in mixture_files.readlines()]

    for group_id in range(num_groups):
        start_idx = group_id * group_size
        end_idx = start_idx + group_size
        group_original_paths = original_paths[start_idx:end_idx]
        group_enhanced_paths = enhanced_paths[start_idx:end_idx]
        group_mixture_paths = mixture_paths[start_idx:end_idx]

        series_list = []
        for original_path, enhanced_path, mixture_path in tqdm(zip(group_original_paths, group_enhanced_paths, group_mixture_paths), total=group_size):
            # Load audio files
            source_np, _ = sf.read(original_path)
            est_source_np, _ = sf.read(enhanced_path)
            mixture_np, _ = sf.read(mixture_path)

            utt_metrics = get_metrics(
                mixture_np,  # 実際の混合音を使用
                source_np,
                est_source_np,
                sample_rate=conf["sample_rate"],
                metrics_list=conf["compute_metrics"],
            )

            series_list.append(pd.Series(utt_metrics))

        # Calculate the average metrics for the current group
        group_metrics_df = pd.DataFrame(series_list)
        final_results = {}
        for metric_name in conf["compute_metrics"]:
            final_results[metric_name] = group_metrics_df[metric_name].mean()

        # Store results for the current group in the global dictionary
        all_group_results[f"Group_{group_id + 1}"] = final_results

# Initialize a dictionary to store the overall average metrics
overall_average_metrics = {}

# Loop through each metric name
for metric_name in conf["compute_metrics"]:
    # Initialize a variable to keep track of the sum of the metric values
    metric_sum = 0
    # Loop through each group result and add the metric value to the sum
    for group_id in range(num_groups):
        metric_sum += all_group_results[f"Group_{group_id + 1}"][metric_name]
    # Calculate the average metric value across all groups
    overall_average_metrics[metric_name] = metric_sum / num_groups

# Store the overall average metrics in the all_group_results dictionary
all_group_results['Overall_Average'] = overall_average_metrics

# Save all groups' metrics and the overall average metrics to a single JSON file
with open(os.path.join(eval_save_dir, "IVA_test_sub1.0"), "w") as f:
    json.dump(all_group_results, f, indent=2)

