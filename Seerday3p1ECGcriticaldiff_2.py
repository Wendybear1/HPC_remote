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
from scipy.signal import butter, lfilter
from datetime import datetime
from biosppy.signals import ecg
import pandas as pd

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



# import os
# channel_arr = []
# directory =r'/fred/oz132/DownloadEEG/NSW0352'
#
# dir_list = list(os.scandir(directory))
# dir_list.sort(key=lambda d:d.path)
# for entry in dir_list:
#     if (entry.path.endswith(".csv")) and entry.is_file():
#         raw_ecg = pd.read_csv(entry.path, skipinitialspace=True)
#         target_signal_1 = raw_ecg.T4
#         channel_arr = channel_arr + list(target_signal_1)
#
# ch_filtered = butter_bandpass_filter(channel_arr, 1, 30, 256, order=5)
# ch_notch = Implement_Notch_Filter(256, 5, 50, 3, 5, 'butter', ch_filtered)
#
#
#
# signal=ch_notch
# divsignal_arr=split(signal,256*15)
#
# target_signal_arr=[]
# for i in range(len(divsignal_arr)):
#     target_signal_arr.append(divsignal_arr[i][0:256*15])
#
# value_arr=[]
# variance_arr=[]
# value_lag_arr=[]
# for k in range(len(target_signal_arr)):
#     x = target_signal_arr[k]
#     y = target_signal_arr[k] - target_signal_arr[k].mean()
#     target_signal_std = np.std(target_signal_arr[k])
#     target_signal_var=target_signal_std**2
#     variance_arr.append(target_signal_var)
#     y = y / target_signal_std
#     R = np.correlate(y, y, mode='full')/len(x)
#     for k in range(len(R)):
#         if R[k] < 0.5 * R.max():
#             k = k + 1
#         else:
#             indice1 = k
#             indice2 = len(R) - indice1
#             value = indice2 - indice1
#             value_arr.append(value)
#             break
#     for k in range(len(R)):
#         if R[k] == R.max():
#             value_lag_arr.append(R[k+1])
# np.savetxt("T4_EEGvariance_NSW0352_15s_3h.csv", variance_arr, delimiter=",", fmt='%s')
# np.savetxt("T4_EEGauto_NSW0352_15s_3h.csv", value_arr, delimiter=",", fmt='%s')
# # np.savetxt("T3_EEGauto_lag1_NSW0352_15s_3h.csv", value_arr, delimiter=",", fmt='%s')


import pandas as pd
import os
data_pre=[]
channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
for m in range(len(channel)):
    channel_arr = []
    directory =r'/fred/oz132/DownloadEEG/QLD0290'
    dir_list = list(os.scandir(directory))
    dir_list.sort(key=lambda d:d.path)
    for entry in dir_list:
        if (entry.path.endswith(".csv")) and entry.is_file():
            raw_ecg = pd.read_csv(entry.path, skipinitialspace=True)
            ch=channel[m]
            target_signal_1 = raw_ecg[ch]
            channel_arr = channel_arr + list(target_signal_1)

    index = [5468,10332,11682,15941,22516,28271,29126,33686,34127]
    # index = [1520, 2818, 4366, 7590, 9973, 10516, 12303, 13670]
    signal_select=[]
    for j in range(len(index)):
        signal_select =signal_select+channel_arr[(index[j] * 15 * 256):(index[j] * 15 + 120) * 256]

    data_pre.append(signal_select)


import pandas as pd
df = pd.DataFrame()
channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
for i in range(len(data_pre)):
    df[channel[i]]=data_pre[i]

df.to_csv("/home/wxiong/seer_remote/eeg_data_result/channels/EEGraw_QLD0290.csv")
