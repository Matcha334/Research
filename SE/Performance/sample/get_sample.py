import glob
import shutil
import os

# MUBASEディレクトリのパス
sound_dir1 = '/mnt/kiso-qnap/thayashi/data/IVA_RoomSim/Libri2Mix-base/test/IVA/GaussModel/1221-135767-0008_3570-5695-0015.wav'
sound_dir2 = '/mnt/kiso-qnap/thayashi/data/MBS_RoomSim/Libri2Mix-base/test/MBS_TS_imp_1.0/ase/1221-135767-0008_3570-5695-0015.wav'


# ファイルをコピーする先のディレクトリのパス
des_dir1 = 'IVA/back'
des_dir2 = 'MUBASE/back'

# source_dirから全ての.wavファイルを取得
wav_files = []
wav_files.append(sound_dir1)
wav_files.append(sound_dir2)


shutil.copy2(sound_dir1, des_dir1)
shutil.copy2(sound_dir2, des_dir2)


"""
# 各.wavファイルに対して
for file in wav_files:
    # ファイルをdestination_dirにコピー
    shutil.copy2(file, destination_dir)
"""