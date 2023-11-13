from __future__ import division
import mne
import numpy as np
import scipy.signal
from scipy.signal import butter, lfilter
from matplotlib import pyplot
import math
from scipy.fftpack import fft, ifft
from scipy import signal
from scipy.signal import butter, lfilter, iirfilter, filtfilt
from scipy.signal import hilbert
from biosppy.signals import tools
import pandas as pd
from matplotlib import rc
import csv
from biosppy.signals import ecg

from six.moves import range, zip


# local
from biosppy.signals import tools as st
from biosppy.signals.tools import utils

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
    nyq  = fs/2.0
    low  = freq - band/2.0
    high = freq + band/2.0
    low  = low/nyq
    high = high/nyq
    b, a = iirfilter(order, [low, high], rp=ripple, btype='bandstop',analog=False, ftype=filter_type)
    filtered_data = lfilter(b, a, data)
    return filtered_data

def movingaverage(values, window_size):
    weights = (np.ones(window_size))/window_size
    a=np.ones(1)
    return lfilter(weights,a,values)

def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:(size+1)]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs



import os
channel_arr = []
value_arr=[]
variance_arr=[]
directory = r'/fred/oz132/Download/QLD0960'


target_signal_arr_ch1 = []
target_signal_arr_ch2 = []
target_signal_arr_ch3 = []
dir_list = list(os.scandir(directory))
dir_list.sort(key=lambda d:d.path)
for entry in dir_list:
    if (entry.path.endswith(".csv")) and entry.is_file():
        raw_ecg = pd.read_csv(entry.path, skipinitialspace=True)
        target_signal_1 = raw_ecg.ECG1
        target_signal_2 = raw_ecg.ECG2
        target_signal_3 = raw_ecg.ECG3
        target_signal_arr_ch1 = target_signal_arr_ch1 + list(target_signal_1)
        target_signal_arr_ch2 = target_signal_arr_ch2 + list(target_signal_2)
        target_signal_arr_ch3 = target_signal_arr_ch3 + list(target_signal_3)

subtract_3_1 = np.array(target_signal_arr_ch3) - np.array(target_signal_arr_ch1)
subtract_2_1 = np.array(target_signal_arr_ch2) - np.array(target_signal_arr_ch1)

signal = subtract_2_1
divsignal_arr = split(signal, 256 * 15)
hr_31_arr = []
ts_31_arr=[]
for i in range(len(divsignal_arr)):
        target_signal_arr = divsignal_arr[i]
        hr_ts_31, hr_31 = ecg.ecg(signal=target_signal_arr, sampling_rate=256, show=False)[5:7]
        hr_31_arr.append(hr_31)
        ts_31_arr.append(hr_ts_31+15*i)

# np.savetxt("hr_ts_ch21_QLD0960_15s_3h.csv", ts_31_arr, delimiter=",", fmt='%s')
# np.savetxt("hr_ch21_timearr_QLD0960_15s_3h.csv", hr_31_arr, delimiter=",", fmt='%s')

df = pd.DataFrame(data={"time": ts_31_arr, "hr": hr_31_arr})
df.to_csv("hr_ch31_QLD0960_15s_3h./file.csv", sep=',',index=False)