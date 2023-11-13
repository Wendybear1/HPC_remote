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
import datetime
import pytz
import matplotlib.dates as mdates

def butter_bandpass(lowcut, highcut, fs,order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs,order):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def Implement_Notch_Filter(fs, band, freq, ripple, order, filter_type, data):
    nyq = fs / 2.0
    low = freq - band / 2.0
    high = freq + band / 2.0
    low = low / nyq
    high = high / nyq
    b, a = iirfilter(order, [low, high], rp=ripple, btype='bandstop', analog=False, ftype=filter_type)
    filtered_data = filtfilt(b, a, data)
    return filtered_data


def sliding_window(elements, window_size,overlap):
    # if len(elements) <= window_size:
    #     # segment_arr.append(elements)
    #     return elements
    segment_arr = []
    for i in range(0,len(elements),overlap):
        # print(elements[i:i + window_size])
        segment_arr.append(elements[i:i + window_size])
    return segment_arr




# Fs = 256
# f = 1
# sample = 256*10
# x1 = np.arange(sample)
# y1 = np.sin(2 * np.pi * f * x1 / Fs)
# Fs = 256
# f = 1.5
# sample = 256*10
# x2 = np.arange(sample)
# y2 = np.sin(2 * np.pi * f * x2 / Fs)
# y=y1+y2
# pyplot.plot(x1, y,'k',label='delta')
# Fs = 256
# f = 15
# sample = 256*10
# x3 = np.arange(sample)
# y3 = np.sin(2 * np.pi * f * x3 / Fs)
# y=y1+y2+y3
# pyplot.plot(x1, y,'grey',label='noised')
# sig_filtered = butter_bandpass_filter(y, 0.5, 2, 256, order=4)
# pyplot.plot(x1, sig_filtered,'r', label='filtered')
# pyplot.xlabel('sample(n)')
# pyplot.ylabel('voltage(V)')
# pyplot.legend()
# pyplot.show()


import os
channel = ['Fz', 'C4', 'Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8',
           'T6', 'T5', 'Cz']
# for i in range(len(channel)):
for i in range(1,2):
    channel_arr = []
    directory = r'/fred/oz132/DownloadEEG/ACT0128/night'
    dir_list = list(os.scandir(directory))
    dir_list.sort(key=lambda d: d.path)
    for entry in dir_list:
        if (entry.path.endswith(".csv")) and entry.is_file():
            raw_ecg = pd.read_csv(entry.path, skipinitialspace=True)
            ch = channel[i]
            target_signal = raw_ecg[ch].values*(10**6)
            epoch_time = raw_ecg['time'].values

            # df = pd.DataFrame(list(zip(epoch_time, target_signal)), columns=['time', 'wave'])
            # df['time'] = pd.to_datetime(df['time'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Australia/Sydney')
            # pyplot.plot(df['time'].values, df['wave'].values)
            # pyplot.ylabel('$\mathregular{\u03BCV}$',fontsize=10)
            # pyplot.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M', tz=pytz.timezone('Australia/Sydney')))
            # pyplot.show()

            segment=sliding_window(target_signal, 256*60*10,256*60*5)
            time_0=epoch_time[0]

            signal_arr=[]
            time_arr=[]
            for m in range(len(segment)):
            #for m in range(1):
                sig_filtered = butter_bandpass_filter(segment[m], 0.5, 2, 256, order=4)

                time=np.linspace(int(time_0/1000), int(time_0/1000) + 10*60, len(sig_filtered))
                print(len(time))

                df = pd.DataFrame(list(zip(time, sig_filtered)), columns=['time', 'wave'])
                df['time'] = pd.to_datetime(df['time'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Australia/Sydney')
                print(time[0]);print(time[-1]);
                pyplot.plot(df['time'].values, df['wave'].values)
                pyplot.legend([f'{ch}'])
                pyplot.gca().xaxis.set_major_formatter(
                    mdates.DateFormatter('%H:%M', tz=pytz.timezone('Australia/Sydney')))
                pyplot.savefig(f'/fred/oz132/DownloadEEG/ACT0128/night/figure/{m}.png')
                #pyplot.show()

                # pyplot.plot(df['time'].values[93600:113600], df['wave'].values[93600:113600])
                # pyplot.legend([f'{ch}'])
                # pyplot.gca().xaxis.set_major_formatter(
                #     mdates.DateFormatter('%H:%M', tz=pytz.timezone('Australia/Sydney')))
                # # pyplot.savefig(f'C:/Users/wxiong/PycharmProjects/ML/delta/figure/{m}.png')
                # pyplot.show()

                time_0 = time_0 + 5 * 60000
                print(time_0)