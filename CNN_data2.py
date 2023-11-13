from __future__ import division
import pandas as pd
import numpy as np
import os


## prepare for CNN
X_matrice=[]
Y_matrice=[]
directory =r'/fred/oz132/EEG_ML/30minpreictal/ES'
dir_list = list(os.scandir(directory))
dir_list.sort(key=lambda d:d.path)
for entry in dir_list:
    if (entry.path.endswith(".csv")) and entry.is_file():
        dataset = pd.read_csv(entry.path, sep=',',skipinitialspace=True)
        for m in range(int(len(dataset)/(256*15))):
        # for m in range(1):
            # for i in range(0+256*15*m,256*15*1+256*15*m):
            # for i in range(1):
            i=256*15*m
            matrix = [
                [dataset.loc[i, :]['F7'], dataset.loc[i, :]['F3'], dataset.loc[i, :]['Fz'], dataset.loc[i, :]['F4'],
                 dataset.loc[i, :]['F8']],
                [dataset.loc[i, :]['T3'], dataset.loc[i, :]['C3'], dataset.loc[i, :]['Cz'], dataset.loc[i, :]['C4'],
                 dataset.loc[i, :]['T4']],
                [dataset.loc[i, :]['T5'], dataset.loc[i, :]['P3'], dataset.loc[i, :]['Pz'], dataset.loc[i, :]['P4'],
                 dataset.loc[i, :]['T6']],
                [0 * i, dataset.loc[i, :]['O1'], 0 * i, dataset.loc[i, :]['O2'], 0 * i]]
            X_matrice.append(matrix)
        Y_matrice.append(1)
# print(X_matrice)
# print(Y_matrice)
X_matrice=np.array(X_matrice)
# print(X_matrice.shape)
import itertools
data  = list(itertools.chain(*X_matrice))
df = pd.DataFrame.from_records(data)
df['label']=np.ones(len(df))
# print(df)
df.to_csv("/fred/oz132/EEG_ML/30minpreictal/data_ES_preictal_30min_CNN.csv")

import os
X_matrice=[]
Y_matrice=[]
directory =r'/fred/oz132/EEG_ML/30minpreictal/PNES'
dir_list = list(os.scandir(directory))
dir_list.sort(key=lambda d:d.path)
for entry in dir_list:
    if (entry.path.endswith(".csv")) and entry.is_file():
        dataset = pd.read_csv(entry.path, sep=',',skipinitialspace=True)
        for m in range(int(len(dataset)/(256*15))):
        # for m in range(1):
            # for i in range(0+256*15*m,256*60*1+256*15*m):
            # for i in range(1):
            i = 256 * 15 * m
            matrix = [
                [dataset.loc[i, :]['F7'], dataset.loc[i, :]['F3'], dataset.loc[i, :]['Fz'], dataset.loc[i, :]['F4'],
                 dataset.loc[i, :]['F8']],
                [dataset.loc[i, :]['T3'], dataset.loc[i, :]['C3'], dataset.loc[i, :]['Cz'], dataset.loc[i, :]['C4'],
                 dataset.loc[i, :]['T4']],
                [dataset.loc[i, :]['T5'], dataset.loc[i, :]['P3'], dataset.loc[i, :]['Pz'], dataset.loc[i, :]['P4'],
                 dataset.loc[i, :]['T6']],
                [0 * i, dataset.loc[i, :]['O1'], 0 * i, dataset.loc[i, :]['O2'], 0 * i]]
            X_matrice.append(matrix)
        Y_matrice.append(1)
# print(X_matrice)
# print(Y_matrice)
X_matrice=np.array(X_matrice)
# print(X_matrice.shape)

import itertools
data  = list(itertools.chain(*X_matrice))
df = pd.DataFrame.from_records(data)
df['label']=np.zeros(len(df))
# print(df)
df.to_csv("/fred/oz132/EEG_ML/30minpreictal/data_PNES_preictal_30min_CNN.csv")



