from __future__ import division
import mne
import numpy as np
import scipy.signal
from matplotlib import pyplot
import math
from scipy.fftpack import fft, ifft
from scipy import signal
from scipy.signal import hilbert
from scipy.signal import butter, lfilter, iirfilter
from biosppy.signals import tools

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
def Implement_Notch_Filter(fs, band, freq, ripple, order, filter_type, data):
    nyq = fs / 2.0
    low = freq - band / 2.0
    high = freq + band / 2.0
    low = low / nyq
    high = high / nyq
    b, a = iirfilter(order, [low, high], rp=ripple, btype='bandstop', analog=False, ftype=filter_type)
    filtered_data = lfilter(b, a, data)
    return filtered_data
def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs
def movingaverage(values, window_size):
    weights = (np.ones(window_size))/window_size
    a=np.ones(1)
    return lfilter(weights,a,values)



import pandas as pd
import os


import os

# directory =r'/fred/oz132/QLD1282'
# data_pre=[]
# data_interictal =[]
# for i in range(21):
#     signal_channel = []
#     dir_list = list(os.scandir(directory))
#     dir_list.sort(key=lambda d:d.path)
#     channel_arr=[]
#     for entry in dir_list:
#         if (entry.path.endswith("EEG.edf")
#             or entry.path.endswith("EEG.edf")) and entry.is_file():
#                 raw_eeg = mne.io.read_raw_edf(entry.path, preload=True)
#                 target_signal = list(raw_eeg._data[i])
#                 channel_arr = channel_arr + target_signal
#
#
#     # index = [1487, 3829, 5081, 7195,10117, 12498, 15489, 18697, 21542, 24461, 27043, 29002, 29974] ## SA0124
#     # index = [1020,1958,6712,9530,12549,13636,18130,20847,22055,22889,26682,28297,32575]
#     index = [437, 1599, 4542, 5841, 7122, 10495, 10646, 11803, 13146,
#              16584,17723,22917,23367,23778,24583,28886,29797,33430,34921,35917] ## QLD1282
#
#     signal_select=[]
#     for j in range(len(index)):
#         # signal_select =signal_select+channel_arr[(index[j] * 15 * 256):(index[j] * 15 + 120) * 256]
#         signal_select = signal_select + channel_arr[(index[j] * 15 - 15 * 60) * 256:(index[j] * 15 * 256)]
#     data_pre.append(signal_select)
#
#     signal_select_interictal = []
#     for j in range(len(index)):
#         if index[j] * 15 - 75 * 60>0:
#             signal_select_interictal = signal_select_interictal + channel_arr[(index[j] * 15 - 75 * 60) * 256:(index[j] * 15 - 60 * 60) * 256]
#     data_interictal.append(signal_select_interictal)
#
#
# import pandas as pd
# df = pd.DataFrame()
# channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
# for i in range(len(data_pre)):
#     df[channel[i]]=data_pre[i]
# df.to_csv("/fred/oz132/EEG_ML/EEG_preictal_QLD1282.csv")
#
# df = pd.DataFrame()
# channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
# for i in range(len(data_interictal)):
#     df[channel[i]]=data_interictal[i]
# df.to_csv("/fred/oz132/EEG_ML/EEG_interictal_QLD1282.csv")




import pandas as pd

import os

data_pre_15min = []
data_pre_30min = []
data_pre_45min = []
data_pre_60min = []
data_interictal = []
channel = ['Fz', 'C4', 'Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8',
           'T6', 'T5', 'Cz']
for m in range(len(channel)):
    channel_arr = []
    directory = r'/fred/oz132/DownloadEEG/VIC0829'
    dir_list = list(os.scandir(directory))
    dir_list.sort(key=lambda d: d.path)
    for entry in dir_list:
        if (entry.path.endswith(".csv")) and entry.is_file():
            raw_ecg = pd.read_csv(entry.path, skipinitialspace=True)
            ch = channel[m]
            target_signal_1 = raw_ecg[ch]
            channel_arr = channel_arr + list(target_signal_1)

    # index = [5468, 10332, 11682, 15941, 22516, 28271, 29126, 33686, 34127]  ## QLD0290
    index = [586, 6872, 10359, 16528, 33444, 34881, 36505, 38528]  ## VIC0829
    # index = [1083,4491,5403,6715,8379,12191,13651,17035,18131,19667,24319,26047,31751,35043,35968] ## VIC0583
    # index = [1701, 6781, 11290, 13475, 18450, 23500, 28619]  ## ACT0128
    # index = [267, 998, 1193, 3252, 7014, 10660, 12255, 17875, 24345]  ## QLD1230
    # index = [437, 1599, 4542, 5841, 7122, 10495, 10646, 11803, 13146, 16584,17723,22917,23367,23778,24583,28886,29797,33430,34921,35917] # QLD1282
    # index = [1725, 6404, 7544, 11031, 12172, 13210, 16833, 18091, 23413, 24151, 24630, 30491, 35372,
    #          36202, 36486]  ### vic2037
    # index = [1520, 2818, 4366, 7590, 9973, 10516, 12303, 13670] ## VIC2835
    # index = [2774, 7912, 13139, 16795, 22656, 26133] # SA1243 edf
    # index = [1204, 6089, 11219, 28978, 31944]  ## VIC0821

    signal_select = []
    for j in range(len(index)):
        # signal_select =signal_select+channel_arr[(index[j] * 15 * 256):(index[j] * 15 + 120) * 256]
        signal_select = signal_select + channel_arr[(index[j] * 15 - 15 * 60) * 256:(index[j] * 15 * 256)]
    data_pre_15min.append(signal_select)

    signal_select = []
    for j in range(len(index)):
        signal_select = signal_select + channel_arr[(index[j] * 15 - 30 * 60) * 256:(index[j] * 15 - 15 * 60) * 256]
    data_pre_30min.append(signal_select)

    signal_select = []
    for j in range(len(index)):
        signal_select = signal_select + channel_arr[(index[j] * 15 - 45 * 60) * 256:(index[j] * 15 - 30 * 60) * 256]
    data_pre_45min.append(signal_select)

    signal_select = []
    for j in range(len(index)):
        signal_select = signal_select + channel_arr[(index[j] * 15 - 60 * 60) * 256:(index[j] * 15 - 45 * 60) * 256]
    data_pre_60min.append(signal_select)

    # signal_select_interictal = []
    # for j in range(len(index)):
    #     signal_select_interictal = signal_select_interictal + channel_arr[(index[j] * 15 - 75 * 60) * 256:(index[
    #                                                                                                            j] * 15 - 15 * 60) * 256]
    # data_interictal.append(signal_select)

import pandas as pd

df = pd.DataFrame()
channel = ['Fz', 'C4', 'Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8',
           'T6', 'T5', 'Cz']
for i in range(len(data_pre_15min)):
    df[channel[i]] = data_pre_15min[i]
df.to_csv("/fred/oz132/EEG_ML/15minpreictal/EEG_preictal_VIC0829.csv")

for i in range(len(data_pre_30min)):
    df[channel[i]] = data_pre_30min[i]
df.to_csv("/fred/oz132/EEG_ML/30minpreictal/EEG_preictal_VIC0829.csv")

for i in range(len(data_pre_45min)):
    df[channel[i]] = data_pre_45min[i]
df.to_csv("/fred/oz132/EEG_ML/45minpreictal/EEG_preictal_VIC0829.csv")

for i in range(len(data_pre_60min)):
    df[channel[i]] = data_pre_60min[i]
df.to_csv("/fred/oz132/EEG_ML/60minpreictal/EEG_preictal_VIC0829.csv")




data_pre_15min = []
data_pre_30min = []
data_pre_45min = []
data_pre_60min = []
data_interictal = []
channel = ['Fz', 'C4', 'Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8',
           'T6', 'T5', 'Cz']
for m in range(len(channel)):
    channel_arr = []
    directory = r'/fred/oz132/DownloadEEG/VIC0583'
    dir_list = list(os.scandir(directory))
    dir_list.sort(key=lambda d: d.path)
    for entry in dir_list:
        if (entry.path.endswith(".csv")) and entry.is_file():
            raw_ecg = pd.read_csv(entry.path, skipinitialspace=True)
            ch = channel[m]
            target_signal_1 = raw_ecg[ch]
            channel_arr = channel_arr + list(target_signal_1)

    # index = [5468, 10332, 11682, 15941, 22516, 28271, 29126, 33686, 34127]  ## QLD0290
    # index = [586, 6872, 10359, 16528, 33444, 34881, 36505, 38528]  ## VIC0829
    index = [1083,4491,5403,6715,8379,12191,13651,17035,18131,19667,24319,26047,31751,35043,35968] ## VIC0583
    # index = [1701, 6781, 11290, 13475, 18450, 23500, 28619]  ## ACT0128
    # index = [267, 998, 1193, 3252, 7014, 10660, 12255, 17875, 24345]  ## QLD1230
    # index = [437, 1599, 4542, 5841, 7122, 10495, 10646, 11803, 13146, 16584,17723,22917,23367,23778,24583,28886,29797,33430,34921,35917] # QLD1282
    # index = [1725, 6404, 7544, 11031, 12172, 13210, 16833, 18091, 23413, 24151, 24630, 30491, 35372,
    #          36202, 36486]  ### vic2037
    # index = [1520, 2818, 4366, 7590, 9973, 10516, 12303, 13670] ## VIC2835
    # index = [2774, 7912, 13139, 16795, 22656, 26133] # SA1243 edf
    # index = [1204, 6089, 11219, 28978, 31944]  ## VIC0821

    signal_select = []
    for j in range(len(index)):
        # signal_select =signal_select+channel_arr[(index[j] * 15 * 256):(index[j] * 15 + 120) * 256]
        signal_select = signal_select + channel_arr[(index[j] * 15 - 15 * 60) * 256:(index[j] * 15 * 256)]
    data_pre_15min.append(signal_select)

    signal_select = []
    for j in range(len(index)):
        signal_select = signal_select + channel_arr[(index[j] * 15 - 30 * 60) * 256:(index[j] * 15 - 15 * 60) * 256]
    data_pre_30min.append(signal_select)

    signal_select = []
    for j in range(len(index)):
        signal_select = signal_select + channel_arr[(index[j] * 15 - 45 * 60) * 256:(index[j] * 15 - 30 * 60) * 256]
    data_pre_45min.append(signal_select)

    signal_select = []
    for j in range(len(index)):
        signal_select = signal_select + channel_arr[(index[j] * 15 - 60 * 60) * 256:(index[j] * 15 - 45 * 60) * 256]
    data_pre_60min.append(signal_select)

    # signal_select_interictal = []
    # for j in range(len(index)):
    #     signal_select_interictal = signal_select_interictal + channel_arr[(index[j] * 15 - 75 * 60) * 256:(index[
    #                                                                                                            j] * 15 - 15 * 60) * 256]
    # data_interictal.append(signal_select)

import pandas as pd

df = pd.DataFrame()
channel = ['Fz', 'C4', 'Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8',
           'T6', 'T5', 'Cz']
for i in range(len(data_pre_15min)):
    df[channel[i]] = data_pre_15min[i]
df.to_csv("/fred/oz132/EEG_ML/15minpreictal/EEG_preictal_VIC0583.csv")

for i in range(len(data_pre_30min)):
    df[channel[i]] = data_pre_30min[i]
df.to_csv("/fred/oz132/EEG_ML/30minpreictal/EEG_preictal_VIC0583.csv")

for i in range(len(data_pre_45min)):
    df[channel[i]] = data_pre_45min[i]
df.to_csv("/fred/oz132/EEG_ML/45minpreictal/EEG_preictal_VIC0583.csv")

for i in range(len(data_pre_60min)):
    df[channel[i]] = data_pre_60min[i]
df.to_csv("/fred/oz132/EEG_ML/60minpreictal/EEG_preictal_VIC0583.csv")










# import pandas as pd
#
# import os
#
# data_pre=[]
# data_interictal=[]
# channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
# for m in range(len(channel)):
#     channel_arr = []
#     directory =r'/fred/oz132/DownloadEEG/QLD0290'
#     dir_list = list(os.scandir(directory))
#     dir_list.sort(key=lambda d:d.path)
#     for entry in dir_list:
#         if (entry.path.endswith(".csv")) and entry.is_file():
#             raw_ecg = pd.read_csv(entry.path, skipinitialspace=True)
#             ch=channel[m]
#             target_signal_1 = raw_ecg[ch]
#             channel_arr = channel_arr + list(target_signal_1)
#     index = [5468, 10332, 11682, 15941, 22516, 28271, 29126, 33686, 34127]  ## QLD0290
#     # index = [586, 6872, 10359, 16528, 33444, 34881, 36505, 38528]  ## VIC0829
#     # index = [1083,4491,5403,6715,8379,12191,13651,17035,18131,19667,24319,26047,31751,35043,35968] ## VIC0583
#     # index = [1701, 6781, 11290, 13475, 18450, 23500, 28619]  ## ACT0128
#     # index = [267, 998, 1193, 3252, 7014, 10660, 12255, 17875, 24345]  ## QLD1230
#     # index = [437, 1599, 4542, 5841, 7122, 10495, 10646, 11803, 13146, 16584,17723,22917,23367,23778,24583,28886,29797,33430,34921,35917] # QLD1282
#     # index = [1725, 6404, 7544, 11031, 12172, 13210, 16833, 18091, 23413, 24151, 24630, 30491, 35372,
#     #          36202, 36486]  ### vic2037
#     # index = [1520, 2818, 4366, 7590, 9973, 10516, 12303, 13670] ## VIC2835
#     # index = [2774, 7912, 13139, 16795, 22656, 26133] # SA1243
#     ## index = [1204, 6089, 11219, 28978, 31944]  ## VIC0821 edf
#
#
#     signal_select=[]
#     for j in range(len(index)):
#         # signal_select =signal_select+channel_arr[(index[j] * 15 * 256):(index[j] * 15 + 120) * 256]
#         signal_select = signal_select + channel_arr[(index[j] * 15 - 15 * 60) * 256:(index[j] * 15 * 256)]
#     data_pre.append(signal_select)
#
#     signal_select_interictal = []
#     for j in range(len(index)):
#         signal_select_interictal = signal_select_interictal + channel_arr[(index[j] * 15 - 75 * 60) * 256:(index[
#                                                                                                                j] * 15 - 15 * 60) * 256]
#     data_interictal.append(signal_select)
#
# import pandas as pd
# df = pd.DataFrame()
# channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
# for i in range(len(data_pre)):
#     df[channel[i]]=data_pre[i]
#
# df.to_csv("/fred/oz132/EEG_ML/EEG_preictal_QLD0290.csv")
#
# df = pd.DataFrame()
# channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
# for i in range(len(data_interictal)):
#     df[channel[i]]=data_interictal[i]
# df.to_csv("/fred/oz132/EEG_ML/EEG_interictal_QLD0290.csv")



# data_pre=[]
# data_interictal =[]
# channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
# for m in range(len(channel)):
#     channel_arr = []
#     directory =r'/fred/oz132/DownloadEEG/TAS0102'
#     dir_list = list(os.scandir(directory))
#     dir_list.sort(key=lambda d:d.path)
#     for entry in dir_list:
#         if (entry.path.endswith(".csv")) and entry.is_file():
#             raw_ecg = pd.read_csv(entry.path, skipinitialspace=True)
#             ch=channel[m]
#             target_signal_1 = raw_ecg[ch]
#             channel_arr = channel_arr + list(target_signal_1)
#
#     # index = [59, 4976, 15642, 21651, 26941, 32448,33810,38639,44069, 45230,49534]
#     index=[12354,13742,18039,19526,27936,34984]
#     signal_select=[]
#     for j in range(len(index)):
#         # signal_select =signal_select+channel_arr[(index[j] * 15 * 256):(index[j] * 15 + 120) * 256]
#         signal_select = signal_select + channel_arr[(index[j] * 15 - 15 * 60) * 256:(index[j] * 15 * 256)]
#     data_pre.append(signal_select)
#
#     signal_select_interictal = []
#     for j in range(len(index)):
#         signal_select_interictal = signal_select_interictal + channel_arr[(index[j] * 15 - 75 * 60) * 256:(index[j] * 15 - 60 * 60) * 256]
#     data_interictal.append(signal_select_interictal)
#
# import pandas as pd
# df = pd.DataFrame()
# channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
# for i in range(len(data_pre)):
#     df[channel[i]]=data_pre[i]
#
# df.to_csv("/home/wxiong/seer_remote/eeg_data_result//ML_data/EEG_preictal_TAS0102.csv")
#
#
# df = pd.DataFrame()
# channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
# for i in range(len(data_interictal)):
#     df[channel[i]]=data_interictal[i]
# df.to_csv("/home/wxiong/seer_remote/eeg_data_result//ML_data/EEG_interictal_TAS0102.csv")




# import pandas as pd
#
# import os
#
# data_pre=[]
# data_interictal =[]
# channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
# for m in range(len(channel)):
#     channel_arr = []
#     directory =r'/fred/oz132/DownloadEEG/VIC1027'
#     dir_list = list(os.scandir(directory))
#     dir_list.sort(key=lambda d:d.path)
#     for entry in dir_list:
#         if (entry.path.endswith(".csv")) and entry.is_file():
#             raw_ecg = pd.read_csv(entry.path, skipinitialspace=True)
#             ch=channel[m]
#             target_signal_1 = raw_ecg[ch]
#             channel_arr = channel_arr + list(target_signal_1)
#
#     index = [3425, 10184, 11694, 15206, 17250, 20132]
#
#     signal_select=[]
#     for j in range(len(index)):
#         # signal_select =signal_select+channel_arr[(index[j] * 15 * 256):(index[j] * 15 + 120) * 256]
#         signal_select = signal_select + channel_arr[(index[j] * 15 - 15 * 60) * 256:(index[j] * 15 * 256)]
#     data_pre.append(signal_select)
#
#     signal_select_interictal = []
#     for j in range(len(index)):
#         signal_select_interictal = signal_select_interictal + channel_arr[(index[j] * 15 - 75 * 60) * 256:(index[j] * 15 - 60 * 60) * 256]
#     data_interictal.append(signal_select_interictal)
#
# import pandas as pd
# df = pd.DataFrame()
# channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
# for i in range(len(data_pre)):
#     df[channel[i]]=data_pre[i]
#
# df.to_csv("/home/wxiong/seer_remote/eeg_data_result//ML_data/EEG_preictal_VIC1027.csv")
#
#
# df = pd.DataFrame()
# channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
# for i in range(len(data_interictal)):
#     df[channel[i]]=data_interictal[i]
# df.to_csv("/home/wxiong/seer_remote/eeg_data_result//ML_data/EEG_interictal_VIC1027.csv")













