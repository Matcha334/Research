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
mix_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-6spk/anechoic/dev/2spk-mix.txt"
mubase_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-6spk/anechoic/dev/mubase.txt"
multichan_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-6spk/anechoic/dev/4ch-mix.txt"
back_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-6spk/anechoic/dev/back_sph.txt"
target_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-6spk/anechoic/dev/target_sph.txt"
left1_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-6spk/anechoic/dev/left1_sph.txt"
left2_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-6spk/anechoic/dev/left2_sph.txt"
right1_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-6spk/anechoic/dev/right1_sph.txt"
right2_txt = "/mnt/kiso-qnap/thayashi/SE/Performance/data_path/4ch-6spk/anechoic/dev/right2_sph.txt"

txt_path_list = [mix_txt, mubase_txt, multichan_txt, back_txt, target_txt, left1_txt, left2_txt, right1_txt, right2_txt]

# datapath.txtファイルの生成
for txt_path in txt_path_list:
    if not os.path.exists(txt_path):
        with open(txt_path, 'w') as file:
            pass

# 音声ファイルのディレクトリ作成
save_dir = "/mnt/kiso-qnap/thayashi/data/Simulation/Room/4ch-6spk/Libri2Mix-base/anechoic/dev"
mix1_l_dir = os.path.join(save_dir, "observe/mixture/mic_array1/left")
multichan_dir = os.path.join(save_dir, "observe/mixture/4chan")
target_dir = os.path.join(save_dir, "observe/source/target_sph")
back_dir = os.path.join(save_dir, "observe/source/back_sph")
left1_dir = os.path.join(save_dir, "observe/source/left1_sph")
left2_dir = os.path.join(save_dir, "observe/source/left2_sph")
right1_dir = os.path.join(save_dir, "observe/source/right1_sph")
right2_dir = os.path.join(save_dir, "observe/source/right2_sph")
mubase_dir = os.path.join(save_dir, "enhancement/MUBASE/Sub1.0")

seed_counter = 0
    
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
left1_list = []
left2_list = []
right1_list = []
right2_list = []
mubase_list = []
multichan_list = []

for index, target_PATH in enumerate(tqdm(extends_pathline)):
    
    seed_counter = seed_counter + 1
    random.seed(seed_counter)
    path_id = target_PATH.split("/")[-1].split(".")[0]
    target_id = path_id.split("_")[0]
    target_spk = target_id.split("-")[0]
    back_id = path_id.split("_")[1]
    back_spk = back_id.split("-")[0]
    
    #Libri2Mixからランダムに50音声を見つけて, 4人がそれぞれが別話者であることを保証
    noise_PATH_cands = random.sample(corpus_list, 50)
    left_noise1_PATH = None
    left_noise2_PATH = None
    right_noise1_PATH = None
    right_noise2_PATH = None
    
    for noise_path in noise_PATH_cands:
        noise_spk = noise_path.split("/")[-1].split(".")[0].split("_")[0].split("-")[0]
        if (noise_spk != target_spk and noise_spk != back_spk):
            if left_noise1_PATH is None:
                left_noise1_PATH = noise_path
                left_spk1 = noise_spk
            elif (left_noise2_PATH is None and noise_spk != left_spk1):
                left_noise2_PATH = noise_path
                left_spk2 = noise_spk
            elif (right_noise1_PATH is None and noise_spk != left_spk1 and noise_spk != left_spk2):
                right_noise1_PATH = noise_path
                right_spk1 = noise_spk
            elif (right_noise2_PATH is None and noise_spk != left_spk1 and noise_spk != left_spk2 and noise_spk != right_spk1):
                right_noise2_PATH = noise_path
                break
    
    right1_id = right_noise1_PATH.split("/")[-1].split(".")[0].split("_")[0]
    right2_id = right_noise2_PATH.split("/")[-1].split(".")[0].split("_")[0]
    left1_id = left_noise1_PATH.split("/")[-1].split(".")[0].split("_")[0]
    left2_id = left_noise2_PATH.split("/")[-1].split(".")[0].split("_")[0]
    
    mix_path = os.path.join(mix1_l_dir, f"{target_id}_{back_id}_{left1_id}_{left2_id}_{right1_id}_{right2_id}.wav")
    target_path = os.path.join(target_dir, f"{target_id}_{back_id}_{left1_id}_{left2_id}_{right1_id}_{right2_id}.wav")
    back_path = os.path.join(back_dir, f"{target_id}_{back_id}_{left1_id}_{left2_id}_{right1_id}_{right2_id}.wav")
    left1_path = os.path.join(left1_dir, f"{target_id}_{back_id}_{left1_id}_{left2_id}_{right1_id}_{right2_id}.wav")
    left2_path = os.path.join(left2_dir, f"{target_id}_{back_id}_{left1_id}_{left2_id}_{right1_id}_{right2_id}.wav")
    right1_path = os.path.join(right1_dir, f"{target_id}_{back_id}_{left1_id}_{left2_id}_{right1_id}_{right2_id}.wav")
    right2_path = os.path.join(right2_dir, f"{target_id}_{back_id}_{left1_id}_{left2_id}_{right1_id}_{right2_id}.wav")
    mubase_path = os.path.join(mubase_dir, f"{target_id}_{back_id}_{left1_id}_{left2_id}_{right1_id}_{right2_id}.wav")
    multichan_path = os.path.join(multichan_dir, f"{target_id}_{back_id}_{left1_id}_{left2_id}_{right1_id}_{right2_id}.wav")
     
    mix_list.append(mix_path)
    target_list.append(target_path)
    back_list.append(back_path)
    left1_list.append(left1_path)
    left2_list.append(left2_path)
    right1_list.append(right1_path)
    right2_list.append(right2_path)
    mubase_list.append(mubase_path)
    multichan_list.append(multichan_path)
    
        
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
        
with open(left1_txt, 'w') as file:
    for path in left1_list:
        file.write(path + '\n')
        
with open(left2_txt, 'w') as file:
    for path in left2_list:
        file.write(path + '\n')
        
with open(right1_txt, 'w') as file:
    for path in right1_list:
        file.write(path + '\n')
        
with open(right2_txt, 'w') as file:
    for path in right2_list:
        file.write(path + '\n')
        
with open(mubase_txt, 'w') as file:
    for path in mubase_list:
        file.write(path + '\n')