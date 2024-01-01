import csv
import wave
import os
from tqdm import tqdm

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

# mix_dir_path は mixture_same_utt_path.txt　にあるパスで実際のエリア収音のものに変えるためにreplace関数
previous_filename ="/mnt/kiso-qnap/thayashi/data/Simulation/Room/4ch-4spk/Libri2Mix-base/anechoic/test/enhancement/MUBASE/Sub0.7_angle25"
changed_filename = "/mnt/kiso-qnap/thayashi/data/Simulation/Room/4ch-4spk/Libri2Mix-base/anechoic/test/enhancement/MUBASE/Sub0.7_angle35_imp"

previous_file = 'data_path/4ch-4spk/anechoic/test/MUBASE_Sub0.7_angle25.txt'
previous_path_line = read_text_file(previous_file)
        
output_file_path = 'data_path/4ch-4spk/anechoic/test/MUBASE_Sub0.7_angle35_imp.txt'
output_dir = os.path.dirname(output_file_path)

if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 出力ファイルに書き込み
with open(output_file_path, 'w') as file:
    for previous_path in tqdm(previous_path_line):
        changed_path = previous_path.replace(previous_filename, changed_filename)
        file.write(changed_path + '\n')