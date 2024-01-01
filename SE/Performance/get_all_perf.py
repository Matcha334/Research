import json
import os
import soundfile as sf
import numpy as np
import pandas as pd
from asteroid.metrics import get_metrics
from tqdm import tqdm

# Replace these with the path to your files
path_to_original_audio_files = "data_path/IVA/test_s1_path.txt"
path_to_enhanced_audio_files = "data_path/IVA/GaussModel/test_iva_path.txt"

# Set your model sample rate and metrics
conf = {"sample_rate": 8000, "compute_metrics": ["si_sdr", "stoi"]}
eval_save_dir = "results/IVA/GaussModel/test"

# Prepare a global dictionary to store all results
all_group_results = {}

# Split the data into groups of 400 utterances
group_size = 400
num_groups = 15  # Since 6000/400 = 15

with open(path_to_original_audio_files, 'r') as original_files, \
     open(path_to_enhanced_audio_files, 'r') as enhanced_files:

    original_paths = [line.strip() for line in original_files.readlines()]
    enhanced_paths = [line.strip() for line in enhanced_files.readlines()]

    for group_id in range(num_groups):
        start_idx = group_id * group_size
        end_idx = start_idx + group_size
        group_original_paths = original_paths[start_idx:end_idx]
        group_enhanced_paths = enhanced_paths[start_idx:end_idx]

        series_list = []
        for original_path, enhanced_path in tqdm(zip(group_original_paths, group_enhanced_paths), total=group_size):
            # Load audio files
            source_np, _ = sf.read(original_path)
            est_source_np, _ = sf.read(enhanced_path)

            utt_metrics = get_metrics(
                np.zeros_like(source_np),  # dummy mixture (not used in this case)
                source_np,
                est_source_np,
                sample_rate=conf["sample_rate"],
                metrics_list=conf["compute_metrics"],
            )
            if isinstance(utt_metrics, pd.Series):
                utt_metrics = utt_metrics.to_dict()

            metrics_with_path = utt_metrics  # Start with metrics
            metrics_with_path["enhanced_path"] = enhanced_path  # Then add the enhanced_path

            series_list.append(metrics_with_path)  # Appending the dictionary directly


with open(os.path.join(eval_save_dir, "new_all_perf"), "w") as f:
    for item in series_list:
        # Here, 'item' is already a dictionary, so we convert it to a string format suitable for writing to a file.
        # We use json.dumps() for a cleaner format compared to str().
        f.write(json.dumps(item) + '\n')
