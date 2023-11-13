from __future__ import division
import mne
import numpy as np
import scipy.signal
from scipy.signal import butter, lfilter
from matplotlib import pyplot
import math
from datetime import datetime
import math
from scipy.fftpack import fft, ifft
from scipy import signal
from scipy.signal import butter, lfilter,iirfilter
from biosppy.signals import ecg
import pyhrv

def butter_lowpass(cutoff, fs, order):
    nyq = 0.5 * fs
    normalCutoff = cutoff/ nyq
    b, a = butter(order, normalCutoff, btype='low', analog=True) # butter design an Nth order digital butterworth filter
    return b, a
def butter_lowpass_filter(data, curoff, fs, order):
     b, a = butter_lowpass(curoff, fs, order=order)
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







## plot  day
location =["C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 15.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 15.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 15.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 16.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 16.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 16.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 17.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 17.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 17.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 18.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 18.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 18.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 19.15.48 - ECG.edf", # seizure1
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 19.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 19.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 20.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 20.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 20.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 21.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 21.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 21.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 22.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 22.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 22.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 23.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 23.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.08 23.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 00.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 00.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 00.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 01.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 01.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 01.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 02.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 02.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 02.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 03.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 03.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 03.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 04.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 04.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 04.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 05.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 05.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 05.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 06.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 06.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 06.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 07.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 07.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 07.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 08.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 08.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 08.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 09.15.48 - ECG.edf", # seizure2
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 09.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 09.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 10.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 10.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 10.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 11.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 11.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 11.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 12.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 12.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 12.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 13.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 13.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 13.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 14.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 14.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 14.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 15.15.48 - ECG.edf", #seizure 3
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 15.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 15.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 16.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 16.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 16.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 17.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 17.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 17.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 18.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 18.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 18.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 19.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 19.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 19.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 20.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 20.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 20.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 21.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 21.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 21.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 22.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 22.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 22.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 23.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 23.35.48 - ECG.edf", #seizure 4
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.09 23.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 00.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 00.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 00.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 01.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 01.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 01.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 02.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 02.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 02.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 03.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 03.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 03.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 04.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 04.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 04.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 05.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 05.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 05.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 06.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 06.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 06.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 07.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 07.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 07.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 08.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 08.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 08.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 09.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 09.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 09.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 10.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 10.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 10.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 11.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 11.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 11.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 12.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 12.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 12.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 13.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 13.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 13.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 14.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 14.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 14.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 15.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 15.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 15.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 16.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 16.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 16.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 17.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 17.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 17.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 18.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 18.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 18.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 19.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 19.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 19.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 20.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 20.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 20.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 21.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 21.35.48 - ECG.edf", #seizure 5
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 21.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 22.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 22.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 22.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 23.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 23.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.10 23.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 00.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 00.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 00.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 01.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 01.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 01.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 02.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 02.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 02.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 03.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 03.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 03.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 04.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 04.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 04.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 05.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 05.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 05.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 06.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 06.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 06.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 07.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 07.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 07.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 08.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 08.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 08.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 09.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 09.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 09.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 10.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 10.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 10.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 11.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 11.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 11.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 12.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 12.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 12.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 13.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 13.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 13.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 14.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 14.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 14.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 15.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 15.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 15.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 16.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 16.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 16.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 17.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 17.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 17.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 18.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 18.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 18.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 19.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 19.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 19.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 20.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 20.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 20.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 21.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 21.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 21.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 22.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 22.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 22.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 23.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 23.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.11 23.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 00.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 00.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 00.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 01.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 01.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 01.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 02.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 02.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 02.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 03.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 03.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 03.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 04.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 04.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 04.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 05.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 05.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 05.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 06.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 06.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 06.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 07.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 07.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 07.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 08.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 08.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 08.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 09.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 09.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 09.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 10.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 10.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 10.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 11.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 11.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 11.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 12.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 12.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 12.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 13.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 13.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 13.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 14.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 14.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 14.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 15.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 15.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 15.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 16.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 16.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 16.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 17.15.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 17.35.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 17.55.48 - ECG.edf",
"C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 18.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 18.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 18.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 19.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 19.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 19.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 20.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 20.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 20.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 21.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 21.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 21.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 22.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 22.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 22.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 23.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 23.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.12 23.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 00.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 00.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 00.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 01.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 01.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 01.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 02.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 02.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 02.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 03.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 03.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 03.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 04.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 04.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 04.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 05.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 05.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 05.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 06.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 06.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 06.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 07.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 07.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 07.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 08.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 08.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 08.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 09.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 09.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 09.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 10.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 10.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 10.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 11.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 11.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 11.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 12.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 12.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 12.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 13.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 13.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 13.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 14.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 14.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 14.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 15.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 15.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 15.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 16.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 16.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 16.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 17.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 17.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 17.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 18.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 18.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 18.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 19.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 19.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 19.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 20.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 20.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 20.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 21.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 21.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 21.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 22.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 22.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 22.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 23.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 23.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.13 23.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 00.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 00.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 00.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 01.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 01.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 01.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 02.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 02.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 02.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 03.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 03.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 03.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 04.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 04.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 04.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 05.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 05.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 05.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 06.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 06.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 06.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 07.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 07.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 07.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 08.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 08.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 08.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 09.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 09.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 09.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 10.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 10.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 10.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 11.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 11.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 11.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 12.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 12.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 12.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 13.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 13.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 13.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 14.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 14.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 14.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 15.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 15.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 15.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 16.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 16.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 16.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 17.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 17.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 17.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 18.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 18.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 18.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 19.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 19.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 19.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 20.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 20.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 20.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 21.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 21.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 21.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 22.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 22.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 22.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 23.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 23.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.14 23.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 00.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 00.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 00.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 01.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 01.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 01.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 02.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 02.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 02.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 03.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 03.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 03.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 04.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 04.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 04.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 05.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 05.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 05.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 06.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 06.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 06.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 07.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 07.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 07.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 08.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 08.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 08.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 09.15.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 09.35.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 09.55.48 - ECG.edf",
           "C:/Users/wxiong/Documents/PHD/Seer data/VIC0758/VIC0758 - 19.07.15 10.15.48 - ECG.edf"]

print(len(location))
for j in range(1):
    baseline_arr = []
    seg_arr=[]
    for i in range(216,433): # 216 is forth day,432 is the sixth day
        file = location[i]
        raw_ecg = mne.io.read_raw_edf(file, preload=True)
        target_signal = (raw_ecg._data[j])
        based_sig = butter_lowpass_filter(target_signal, 5, 256, 1)
        detrend_sig = target_signal - based_sig
        powerfiltered_target_sig = Implement_Notch_Filter(256, 5, 50, 3, 5, 'butter', detrend_sig)
        pre_1 = ecg.ecg(signal=powerfiltered_target_sig, sampling_rate=256, show=False)
        # print(len(pre_1[2])),print(len(pre_1[0])), print(pre_1[0]),print(pre_1[2])
        t_R_arr = [] # R time point
        for k in pre_1[2]:
            t_R_arr.append(pre_1[0][k])
        # print(len(t_R_arr))
        inter_arr = [] #RRI array
        for k in range(len(t_R_arr)):
            if k == 0:
                k = k + 1
            else:
                inter_arr.append(t_R_arr[k] - t_R_arr[k - 1])
        # print(len(inter_arr)) # time is t_R_arr[1:]
        # print(inter_arr)  # time is t_R_arr[1:],second
        # print(len(t_R_arr))

        # calculate HR_diff in each segment
        inter_arr_window=[]
        time_arr=[]
        mCSI_arr=[]
        for m in range(3):
            if 100 + 50 * m < len(inter_arr):
                inter_arr_seg=inter_arr[(0+50*m):(100+50*m)] # calculate in each sliding window
                inter_arr_window.append(inter_arr_seg)
                time_arr.append(t_R_arr[m+1])
                result = pyhrv.nonlinear.poincare(inter_arr_seg,show=False)
                # mCSI=float(result['sd2'])*float(result['sd2'])/float(result['sd1'])
                # mCSI_arr.append(mCSI)
                m=m+1
            else:
                break
        # print(len(inter_arr_window)),print(len(time_arr))
        print(mCSI_arr),print(len(mCSI_arr))

        #     HR_diff_value=[]
        #     winindex=[]
        #     for n in range(len(inter_arr_window)):
        #         HR_diff_arr = []
        #         for p in range(1,len(inter_arr_window[n])-1):
        #             if p==0:
        #                 HR_diff_arr.append(inter_arr_window[n][0])
        #             else:
        #                 HR_diff_arr.append(inter_arr_window[n][p+1]-inter_arr_window[n][p-1])
        #         HR_diff=0.5*sum(HR_diff_arr)
        #         HR_diff_value.append(HR_diff)
        #     # print(len(HR_diff_value))
        #     baseline_arr.append(max(HR_diff_value))
        #     baseline_arr.append(min(HR_diff_value))

        # t_arr=[]
        # for time in time_arr:
        #     t_modified=int(time)+20*i
        #     t_arr.append(t_modified)
        # pyplot.plot(t_arr,HR_diff_value,'k')
        pyplot.plot(time_arr,mCSI_arr,'k')
        pyplot.annotate('', xy=(12 * 20 + 7.6, 5), xytext=(12 * 20 + 7.6, 5 + 0.1),
                        arrowprops=dict(facecolor='black', shrink=0.05))
        pyplot.annotate('', xy=(54 * 20 + 10.866, 5), xytext=(54 * 20 + 10.866, 5 + 0.1),
                        arrowprops=dict(facecolor='black', shrink=0.05))
        pyplot.annotate('', xy=(72 * 20 + 15.416, 5), xytext=(72 * 20 + 15.416, 5 + 0.1),
                        arrowprops=dict(facecolor='black', shrink=0.05))
        pyplot.annotate('', xy=(97 * 20 + 6.2667, 5), xytext=(97 * 20 + 6.2667, 5 + 0.1),
                        arrowprops=dict(facecolor='black', shrink=0.05))
        pyplot.annotate('', xy=(163 * 20 + 12.783, 5), xytext=(163 * 20 + 12.783, 5 + 0.1),
                        arrowprops=dict(facecolor='black', shrink=0.05))
        pyplot.xlabel('time(min)')
        # # pyplot.ylabel('HR_diff in three days')
        pyplot.ylabel('modified CSI in three days')
        pyplot.show()
        # # print(max(baseline_arr))
        # # print(min(baseline_arr))
        print(max(mCSI_arr))
