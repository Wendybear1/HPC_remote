from __future__ import division
import mne
import numpy as np
from scipy.signal import butter, filtfilt


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs



# access data
import os
channel_arr = []
directory =r'/fred/oz132/QLD2982'
dir_list = list(os.scandir(directory))
dir_list.sort(key=lambda d:d.path)
for entry in dir_list:
    if (entry.path.endswith("EEG.edf")
        or entry.path.endswith("EEG.edf")) and entry.is_file():
            raw_eeg = mne.io.read_raw_edf(entry.path, preload=True)
            target_signal = list(raw_eeg._data[20])
            channel_arr = channel_arr + target_signal

# filtering
ch_filtered = butter_bandpass_filter(channel_arr, 1, 30, 256, order=5)



# select signal in every 15s
signal=ch_filtered
divsignal_arr=split(signal,256*15)
target_signal_arr=[]
for i in range(len(divsignal_arr)):
    target_signal_arr.append(divsignal_arr[i][0:256*15])


# calcualte variance and autocorrelation
value_arr=[]
variance_arr=[]
value_lag_arr=[]
for k in range(len(target_signal_arr)):
    x = target_signal_arr[k]
    y = target_signal_arr[k] - target_signal_arr[k].mean()
    target_signal_std = np.std(target_signal_arr[k])
    target_signal_var=target_signal_std**2
    variance_arr.append(target_signal_var)
    y = y / target_signal_std
    R = np.correlate(y, y, mode='full')/len(x)
    for k in range(len(R)):
        if R[k] < 0.5 * R.max():
            k = k + 1
        else:
            indice1 = k
            indice2 = len(R) - indice1
            value = indice2 - indice1
            value_arr.append(value)
            break
    for k in range(len(R)):
        if R[k] == R.max():
            value_lag_arr.append(R[k+1])
np.savetxt("/home/wxiong/seer_remote/Cz_EEGvariance_QLD2982_15s.csv", variance_arr, delimiter=",", fmt='%s')
np.savetxt("/home/wxiong/seer_remote/Cz_EEGautoQLD2982_15s.csv", value_arr, delimiter=",", fmt='%s')
np.savetxt("/home/wxiong/seer_remote/Cz_EEGlag1autoQLD2982_15s.csv", value_lag_arr, delimiter=",", fmt='%s')