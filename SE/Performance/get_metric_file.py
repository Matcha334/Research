import json
import os
import soundfile as sf
import numpy as np
import pandas as pd
from asteroid.metrics import get_metrics
from tqdm import tqdm

target_audio_path = "data_path/4ch-4spk/anechoic/test/target_sph.txt"
enhanced_audio_path = "data_path/4ch-4spk/anechoic/test/MUBASE_Sub1.0.txt"

number_of_audio = 500
conf = {"sample_rate": 8000, "compute_metrics": ["si_sdr", "stoi"]}
eval_save_dir = "results/anechoic/4ch-4spk"

all_results = {}

with open(target_audio_path, 'r') as target_files, \
     open(enhanced_audio_path, 'r') as enhanced_files:
         
    target_paths = [line.strip() for line in target_files.readlines()]
    enhanced_paths = [line.strip() for line in enhanced_files.readlines()]
    
    valid_target_paths = target_paths[0:number_of_audio]
    valid_enhanced_paths = enhanced_paths[0:number_of_audio]

    series_list = []
    for target_path, enhanced_path in tqdm(zip(valid_target_paths, valid_enhanced_paths), total=number_of_audio):
        # Load audio files
        source_np, _ = sf.read(target_path)
        est_source_np, _ = sf.read(enhanced_path)

        utt_metrics = get_metrics(
            np.zeros_like(source_np),  # dummy mixture (not used in this case)
            source_np,
            est_source_np,
            sample_rate=conf["sample_rate"],
            metrics_list=conf["compute_metrics"],
        )
        series_list.append(pd.Series(utt_metrics))
        
    metrics_df = pd.DataFrame(series_list)    
    final_results = {}
    for metric_name in conf["compute_metrics"]:
        final_results[metric_name] = metrics_df[metric_name].mean()

    all_results[f"{number_of_audio}_audios_average: "] = final_results
    
    print(all_results)
    
    with open(os.path.join(eval_save_dir, "test_mubase_mixing.json"), "w") as f:
        json.dump(all_results, f, indent=2)   

