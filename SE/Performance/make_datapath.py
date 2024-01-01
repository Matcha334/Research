import numpy as np
import pyroomacoustics as pra
from scipy.io import wavfile
import os
import glob
import random
from tqdm import tqdm
import scipy.signal as sp
import pickle
import soundfile as sf
from scipy.signal import resample_poly
import pandas as pd

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

#データを保存するパス
mix_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-4spk/anechoic/dev/2spk-mix.txt"
mubase_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-4spk/anechoic/dev/MUBASE_Sub1.0.txt"
mubase7_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-4spk/anechoic/dev/MUBASE_Sub0.7.txt"
multichan_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-4spk/anechoic/dev/4ch-mix.txt"
back_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-4spk/anechoic/dev/back_sph.txt"
target_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-4spk/anechoic/dev/target_sph.txt"
left_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-4spk/anechoic/dev/left_sph.txt"
right_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-4spk/anechoic/dev/right_sph.txt"
iva_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-4spk/anechoic/dev/IVA-Gauss50.txt"

save_dir = "/mnt/kiso-qnap/thayashi/data/Simulation/Room/4ch-4spk/Libri2Mix-base/anechoic/dev"
mix1_l_dir = os.path.join(save_dir, "observe/mixture/mic_array1/left")
multichan_dir = os.path.join(save_dir, "observe/mixture/4chan")
target_dir = os.path.join(save_dir, "observe/source/target_sph")
back_dir = os.path.join(save_dir, "observe/source/back_sph")
left_dir = os.path.join(save_dir, "observe/source/left_sph")
right_dir = os.path.join(save_dir, "observe/source/right_sph")
mubase_dir = os.path.join(save_dir, "enhancement/MUBASE/Sub1.0")
mubase7_dir = os.path.join(save_dir, "enhancement/MUBASE/Sub0.7")
iva_dir = os.path.join(save_dir, "enhancement/MUBASE/IVA/Gauss")

seed_counter = 0
s1_path = "/mnt/kiso-qnap/thayashi/LibriMix/storage_dir/Libri2Mix/wav8k/min/dev/s1/"
s2_path = "/mnt/kiso-qnap/thayashi/LibriMix/storage_dir/Libri2Mix/wav8k/min/dev/s2/"
    
#Libri2Mixのパスをリスト化
corpus_txt = '/mnt/kiso-qnap/thayashi/SE/MUBASE/enhancement/Libri2Mix-base/all_path/dev_path.txt'
with open(corpus_txt, 'r') as file:
    corpus_list = [line.strip() for line in file]
    
#Libri2Mixの拡張パスの読み込み   
extends_path_txt = '/mnt/kiso-qnap/thayashi/SE/MUBASE/enhancement/Libri2Mix-base/all_path/dev_extends.txt'
extends_pathline = read_text_file(extends_path_txt)

mix_list = []
target_list = []
back_list = []
left_list = []
right_list = []
mubase_list = []
mubase7_list = []
multichan_list = []
iva_list = []

for index, target_PATH in enumerate(tqdm(extends_pathline[:27000])):
    
    seed_counter = seed_counter + 1
    random.seed(seed_counter)
    path_id = target_PATH.split("/")[-1].split(".")[0]
    target_id = path_id.split("_")[0]
    target_spk = target_id.split("-")[0]
    back_id = path_id.split("_")[1]
    back_spk = back_id.split("-")[0]
    
    #Libri2Mixからランダムに50音声を見つけて, 4人がそれぞれが別話者であることを保証
    noise_PATH_cands = random.sample(corpus_list, 50)
    left_noise_PATH = None
    right_noise_PATH = None
    
    for noise_path in noise_PATH_cands:
        noise_spk = noise_path.split("/")[-1].split(".")[0].split("_")[0].split("-")[0]
        if (noise_spk != target_spk and noise_spk != back_spk):
            if left_noise_PATH is None:
                left_noise_PATH = noise_path
                left_spk = noise_spk
            elif noise_spk != left_spk:
                right_noise_PATH = noise_path
                break
    
    right_id = right_noise_PATH.split("/")[-1].split(".")[0].split("_")[0]
    left_id = left_noise_PATH.split("/")[-1].split(".")[0].split("_")[0]
    
    mix_path = os.path.join(mix1_l_dir, f"{target_id}_{back_id}_{left_id}_{right_id}.wav")
    target_path = os.path.join(target_dir, f"{target_id}_{back_id}_{left_id}_{right_id}.wav")
    back_path = os.path.join(back_dir, f"{target_id}_{back_id}_{left_id}_{right_id}.wav")
    left_path = os.path.join(left_dir, f"{target_id}_{back_id}_{left_id}_{right_id}.wav")
    right_path = os.path.join(right_dir, f"{target_id}_{back_id}_{left_id}_{right_id}.wav")
    mubase_path = os.path.join(mubase_dir, f"{target_id}_{back_id}_{left_id}_{right_id}.wav")
    mubase7_path = os.path.join(mubase7_dir, f"{target_id}_{back_id}_{left_id}_{right_id}.wav")
    multichan_path = os.path.join(multichan_dir, f"{target_id}_{back_id}_{left_id}_{right_id}.wav")
    iva_path = os.path.join(iva_dir, f"{target_id}_{back_id}_{left_id}_{right_id}.wav")
     
    mix_list.append(mix_path)
    target_list.append(target_path)
    back_list.append(back_path)
    left_list.append(left_path)
    right_list.append(right_path)
    mubase_list.append(mubase_path)
    mubase7_list.append(mubase7_path)
    multichan_list.append(multichan_path)
    iva_list.append(iva_path)
        
with open(mix_txt, 'w') as file:
    for path in mix_list:
        file.write(path + '\n')

with open(multichan_txt, 'w') as file:
    for path in multichan_list:
        file.write(path + '\n')
        
with open(target_txt, 'w') as file:
    for path in target_list:
        file.write(path + '\n')
        
with open(back_txt, 'w') as file:
    for path in back_list:
        file.write(path + '\n')
        
with open(left_txt, 'w') as file:
    for path in left_list:
        file.write(path + '\n')
        
with open(right_txt, 'w') as file:
    for path in right_list:
        file.write(path + '\n')
        
with open(mubase_txt, 'w') as file:
    for path in mubase_list:
        file.write(path + '\n')

with open(mubase7_txt, 'w') as file:
    for path in mubase7_list:
        file.write(path + '\n')
        
with open(iva_txt, 'w') as file:
    for path in iva_list:
        file.write(path + '\n')
        

    
        
    