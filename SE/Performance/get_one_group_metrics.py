import json
import os
import soundfile as sf
import numpy as np
import pandas as pd
from asteroid.metrics import get_metrics
from tqdm import tqdm

# Replace these with the path to your files
path_to_original_audio_files = "data_path/IVA/test_s1_path.txt"
path_to_enhanced_audio_files = "data_path/IVA/GaussModel/test_win512_lap384.txt"

# Set your model sample rate and metrics
conf = {"sample_rate": 8000, "compute_metrics": ["si_sdr", "stoi"]}

# Split the data into groups of 400 utterances
group_size = 400
num_groups = 15  # Since 6000/400 = 15

with open(path_to_original_audio_files, 'r') as original_files, \
     open(path_to_enhanced_audio_files, 'r') as enhanced_files:

    original_paths = [line.strip() for line in original_files.readlines()]
    enhanced_paths = [line.strip() for line in enhanced_files.readlines()]

    for group_id in range(1):
        start_idx = group_id * group_size
        end_idx = start_idx + group_size
        group_original_paths = original_paths[start_idx:end_idx]
        group_enhanced_paths = enhanced_paths[start_idx:end_idx]
        
        silent_files = []  # List to store the paths of silent audio files
        series_list = []
        for original_path, enhanced_path in tqdm(zip(group_original_paths, group_enhanced_paths), total=group_size):
            try:
                # Load audio files
                source_np, _ = sf.read(original_path)
                est_source_np, _ = sf.read(enhanced_path)
                
                # Check if the audio is silent
                if np.all(est_source_np == 0):
                    print(f"Found silent audio: {enhanced_path}")
                    silent_files.append(enhanced_path)
                    continue
                
                # Compute metrics
                utt_metrics = get_metrics(
                    np.zeros_like(source_np),  # dummy mixture (not used in this case)
                    source_np,
                    est_source_np,
                    sample_rate=conf["sample_rate"],
                    metrics_list=conf["compute_metrics"],
                )
                series_list.append(pd.Series(utt_metrics))

            except Exception as e:
                print(f"An error occurred while processing file: {enhanced_path}")
                print(f"Error: {e}")

        
        if silent_files:
            print("\nSilent audio files:")
            for path in silent_files:
                print(path)
            
        # Calculate the average metrics for the current group
        group_metrics_df = pd.DataFrame(series_list)
        final_results = {}
        for metric_name in conf["compute_metrics"]:
            final_results[metric_name] = group_metrics_df[metric_name].mean()
        
        print(f'si_sdr: {final_results["si_sdr"]}')
        print(f'stoi: {final_results["stoi"]}')



