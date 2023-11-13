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



location = ["ecg_data_SA0124/SA0124 - 19.08.26 16.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.26 16.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.26 16.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.26 17.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.26 17.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.26 17.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.26 18.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.26 18.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.26 18.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.26 19.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.26 19.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.26 19.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.26 20.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.26 20.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.26 20.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.26 21.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.26 21.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.26 21.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.26 22.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.26 22.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.26 22.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.26 23.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.26 23.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.26 23.55.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 00.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 00.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 00.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 01.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 01.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 01.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 02.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 02.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 02.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 03.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 03.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 03.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 04.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 04.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 04.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 05.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 05.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 05.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 06.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 06.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 06.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 07.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 07.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 07.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 08.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 08.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 08.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 09.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 09.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 09.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 10.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 10.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 10.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 11.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 11.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 11.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 12.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 12.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 12.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 13.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 13.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 13.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 14.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 14.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 14.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 15.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 15.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 15.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 16.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 16.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 16.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 17.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 17.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 17.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 18.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 18.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 18.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 19.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 19.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 19.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 20.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 20.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 20.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 21.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 21.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 21.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 22.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 22.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 22.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 23.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.27 23.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.27 23.55.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 00.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 00.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 00.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 01.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 01.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 01.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 02.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 02.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 02.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 03.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 03.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 03.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 04.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 04.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 04.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 05.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 05.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 05.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 06.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 06.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 06.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 07.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 07.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 07.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 08.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 08.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 08.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 09.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 09.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 09.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 10.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 10.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 10.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 11.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 11.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 11.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 12.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 12.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 12.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 13.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 13.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 13.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 14.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 14.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 14.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 15.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 15.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 15.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 16.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 16.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 16.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 17.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 17.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 17.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 18.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 18.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 18.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 19.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 19.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 19.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 20.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 20.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 20.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 21.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 21.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 21.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 22.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 22.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 22.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 23.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.28 23.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.28 23.55.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 00.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 00.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 00.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 01.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 01.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 01.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 02.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 02.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 02.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 03.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 03.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 03.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 04.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 04.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 04.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 05.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 05.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 05.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 06.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 06.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 06.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 07.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 07.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 07.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 08.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 08.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 08.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 09.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 09.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 09.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 10.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 10.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 10.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 11.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 11.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 11.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 12.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 12.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 12.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 13.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 13.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 13.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 14.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 14.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 14.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 15.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 15.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 15.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 16.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 16.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 16.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 17.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 17.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 17.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 18.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 18.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 18.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 19.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 19.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 19.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 20.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 20.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 20.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 21.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 21.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 21.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 22.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 22.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 22.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 23.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.29 23.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.29 23.55.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 00.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 00.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 00.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 01.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 01.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 01.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 02.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 02.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 02.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 03.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 03.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 03.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 04.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 04.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 04.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 05.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 05.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 05.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 06.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 06.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 06.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 07.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 07.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 07.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 08.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 08.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 08.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 09.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 09.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 09.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 10.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 10.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 10.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 11.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 11.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 11.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 12.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 12.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 12.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 13.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 13.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 13.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 14.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 14.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 14.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 15.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 15.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 15.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 16.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 16.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 16.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 17.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 17.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 17.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 18.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 18.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 18.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 19.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 19.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 19.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 20.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 20.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 20.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 21.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 21.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 21.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 22.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 22.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 22.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 23.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.30 23.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.30 23.55.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 00.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 00.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 00.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 01.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 01.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 01.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 02.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 02.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 02.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 03.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 03.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 03.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 04.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 04.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 04.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 05.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 05.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 05.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 06.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 06.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 06.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 07.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 07.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 07.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 08.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 08.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 08.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 09.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 09.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 09.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 10.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 10.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 10.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 11.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 11.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 11.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 12.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 12.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 12.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 13.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 13.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 13.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 14.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 14.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 14.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 15.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 15.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 15.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 16.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 16.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 16.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 17.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 17.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 17.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 18.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 18.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 18.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 19.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 19.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 19.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 20.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 20.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 20.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 21.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 21.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 21.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 22.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 22.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 22.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 23.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.08.31 23.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.08.31 23.55.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 00.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 00.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 00.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 01.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 01.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 01.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 02.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 02.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 02.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 03.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 03.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 03.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 04.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 04.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 04.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 05.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 05.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 05.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 06.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 06.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 06.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 07.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 07.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 07.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 08.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 08.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 08.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 09.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 09.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 09.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 10.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 10.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 10.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 11.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 11.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 11.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 12.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 12.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 12.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 13.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 13.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 13.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 14.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 14.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 14.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 15.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 15.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 15.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 16.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 16.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 16.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 17.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 17.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 17.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 18.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 18.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 18.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 19.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 19.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 19.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 20.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 20.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 20.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 21.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 21.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 21.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 22.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 22.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 22.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 23.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.01 23.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.01 23.55.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.02 00.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.02 00.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 00.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 01.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.02 01.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 01.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 02.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.02 02.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 02.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 03.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.02 03.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 03.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 04.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.02 04.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 04.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 05.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.02 05.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 05.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 06.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.02 06.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 06.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 07.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.02 07.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 07.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 08.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.02 08.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 08.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 09.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.02 09.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 09.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 10.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.02 10.35.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 10.55.43 - ECG.edf","ecg_data_SA0124/SA0124 - 19.09.02 11.15.43 - ECG.edf",
            "ecg_data_SA0124/SA0124 - 19.09.02 11.35.43 - ECG.edf"]



print(len(location))
for j in range(1,2):
    target_signal_arr = []
    for i in range(len(location)):
        file = location[i]
        raw_ecg = mne.io.read_raw_edf(file, preload=True)
        target_signal = raw_ecg._data[j]
        target_signal_arr = target_signal_arr + list(target_signal)

    ts, signal, pre_1 = ecg.ecg(signal=target_signal_arr, sampling_rate=256, show=False)[0:3]
    t_R_arr_temp = []
    for q in pre_1:
        t_R_arr_temp.append(ts[q])
    RRinter_arr_temp = []
    for k in range(1, len(t_R_arr_temp)):
        RRinter_arr_temp.append(t_R_arr_temp[k] - t_R_arr_temp[k - 1])
    RRinter_arr = []
    t_R_arr = []
    for m in range(len(RRinter_arr_temp)):
        if RRinter_arr_temp[m] <= 1.5 and RRinter_arr_temp[m] >= 0.333:
            RRinter_arr.append(RRinter_arr_temp[m])
            t_R_arr.append(t_R_arr_temp[m + 1])
print(RRinter_arr)
time_modified = []
for i in range(len(t_R_arr)):
    t=time_modified.append(2.98805+t_R_arr[i]/3600)
pyplot.plot(time_modified,RRinter_arr,'k')
pyplot.annotate('',xy=(9.19205,np.max(RRinter_arr)),xytext=(9.19205,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
pyplot.annotate('',xy=(24.16555,np.max(RRinter_arr)),xytext=(24.16555,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
pyplot.annotate('',xy=(32.9738833,np.max(RRinter_arr)),xytext=(32.9738833,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
pyplot.annotate('',xy=(45.149161,np.max(RRinter_arr)),xytext=(45.149161,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
pyplot.annotate('',xy=(55.0694389,np.max(RRinter_arr)),xytext=(55.0694389,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
pyplot.annotate('',xy=(85.90777,np.max(RRinter_arr)),xytext=(85.90777,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
pyplot.annotate('',xy=(92.7538833,np.max(RRinter_arr)),xytext=(92.7538833,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
pyplot.annotate('',xy=(104.916106,np.max(RRinter_arr)),xytext=(104.916106,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
pyplot.annotate('',xy=(139.57055,np.max(RRinter_arr)),xytext=(139.57055,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
pyplot.annotate('',xy=(152.573328,np.max(RRinter_arr)),xytext=(152.573328,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
pyplot.xlabel('time(h)')
pyplot.ylabel('RRI rawsignal in SA0124 2')
pyplot.savefig('RRI rawsignal in SA0124 2')



# Fs = 256
# N = len(RRinter_arr)
# dt = 1 / Fs
# t = np.arange(0, N) * dt
# p = np.polyfit(t, RRinter_arr, 1)
# signal = np.array(RRinter_arr) - np.polyval(p, t)
#
# divsignal_arr=split(signal,50)
# t_div_arr=split(time_modified,50)
#
# target_signal_arr=[]
# for i in range(len(divsignal_arr)):
#     target_signal_arr.append(divsignal_arr[i][0:50])
#
#
# value_arr=[]
# variance_arr=[]
# for k in range(len(target_signal_arr)):
#     x = target_signal_arr[k]
#     y = target_signal_arr[k] - target_signal_arr[k].mean()
#     target_signal_std = np.std(target_signal_arr[k])
#     target_signal_var=target_signal_std**2
#     variance_arr.append(target_signal_var)
#     y = y / target_signal_std
#     R = np.correlate(y, y, mode='full')
#     for k in range(len(R)):
#         if R[k] < 0.5 * R.max():
#             k = k + 1
#         else:
#             indice1 = k
#             indice2 = len(R) - indice1
#             value = indice2 - indice1
#             value_arr.append(value)
#             break
#
# print(variance_arr)
# print(value_arr)
# ## calculate cycles of vairance
# ## smoothing with one day, 1440
# # long_rhythm_var_arr=tools.smoother(variance_arr, kernel='hamming',size=1440*2,mirror=True)
# # short_rhythm_var_arr_show=tools.smoother(variance_arr, kernel='hamming',size=20,mirror=True)
# # short_rhythm_var_arr_show=short_rhythm_var_arr_show[0]
# # short_var_arr=np.array(variance_arr)-np.array(long_rhythm_var_arr[0])
# # short_var_plot=tools.smoother(short_var_arr, kernel='hamming', size=20,mirror=True)
# # short_var_plot=short_var_plot[0]
# # pyplot.figure()
# #
# # t_modified=[]
# # for i in range(len(t_div_arr)):
# #     t_modified.append(t_div_arr[i][0])
# #
# #
# # seizure_timing_index=[]
# # for k in range(len(t_modified)):
# #     if t_modified[k]<9.19205 and t_modified[k+1]>=9.19205:
# #         seizure_timing_index.append(k)
# #     if t_modified[k]<24.16555 and t_modified[k+1]>=24.16555:
# #         seizure_timing_index.append(k)
# #     if t_modified[k]<32.9738833 and t_modified[k+1]>=32.9738833:
# #         seizure_timing_index.append(k)
# #     if t_modified[k]<45.149161 and t_modified[k+1]>=45.149161:
# #         seizure_timing_index.append(k)
# #     if t_modified[k]<55.0694389 and t_modified[k+1]>=55.0694389:
# #         seizure_timing_index.append(k)
# #     if t_modified[k]<85.90777 and t_modified[k+1]>=85.90777:
# #         seizure_timing_index.append(k)
# #     if t_modified[k]<92.7538833 and t_modified[k+1]>=92.7538833:
# #         seizure_timing_index.append(k)
# #     if t_modified[k]<104.916106 and t_modified[k+1]>=104.916106:
# #         seizure_timing_index.append(k)
# #     if t_modified[k]<139.57055 and t_modified[k+1]>=139.57055:
# #         seizure_timing_index.append(k)
# #     if t_modified[k]<152.573328and t_modified[k+1]>=152.573328:
# #         seizure_timing_index.append(k)
# #
# # print(seizure_timing_index)
# #
# #
# #
# #
# #
# # pyplot.plot(t_modified,variance_arr,color=[0.5,0.5,0.5],label='raw RRI variance')
# # pyplot.plot(t_modified,short_rhythm_var_arr_show,'r',alpha=0.5,label='short cycle')
# # pyplot.plot( t_modified,long_rhythm_var_arr[0],'k',label='long cycle')
# # pyplot.legend(loc='upper right')
# # pyplot.annotate('',xy=(9.19205,np.max(variance_arr)),xytext=(9.19205,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(24.16555,np.max(variance_arr)),xytext=(24.16555,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(32.9738833,np.max(variance_arr)),xytext=(32.9738833,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(45.149161,np.max(variance_arr)),xytext=(45.149161,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(55.0694389,np.max(variance_arr)),xytext=(55.0694389,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(85.90777,np.max(variance_arr)),xytext=(85.90777,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(92.7538833,np.max(variance_arr)),xytext=(92.7538833,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(104.916106,np.max(variance_arr)),xytext=(104.916106,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(139.57055,np.max(variance_arr)),xytext=(139.57055,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(152.573328,np.max(variance_arr)),xytext=(152.573328,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.xlabel('time(h)')
# # pyplot.ylabel('variance')
# # pyplot.title('RRI variance in SA0124(smoothing length is one day)')
# # pyplot.savefig('RRI variance in SA 2')
# #
# # # phase analysis
# # var_trans=hilbert(long_rhythm_var_arr[0])
# # var_trans_nomal=[]
# # for m in var_trans:
# #     var_trans_nomal.append(m/abs(m))
# # SIvarlong=sum(var_trans_nomal)/len(var_trans_nomal)
# # print(SIvarlong)
# # seizure_phase=[]
# # for item in seizure_timing_index:
# #     seizure_phase.append(var_trans_nomal[item])
# # SIvarlongseizure=sum(seizure_phase)/len(seizure_phase)
# # print(SIvarlongseizure)
# # var_phase=np.unwrap(np.angle(var_trans))
# #
# # phase_whole_long=[]
# # for i in range(len(var_phase)):
# #     if var_phase[i]<0:
# #         phase_whole_long.append(var_phase[i] + abs((var_phase[i] // (2 * np.pi))) * (2 * np.pi))
# #     elif var_phase[i]>2*np.pi:
# #         phase_whole_long.append(var_phase[i] - (var_phase[i] // (2 * np.pi)) * (2 * np.pi))
# #     else:
# #         phase_whole_long.append(var_phase[i])
# #
# # var_trans=hilbert(short_var_plot)
# # var_trans_nomal=[]
# # for m in var_trans:
# #     var_trans_nomal.append(m/abs(m))
# # SIvarshort=sum(var_trans_nomal)/len(var_trans_nomal)
# # print(SIvarshort)
# # seizure_phase=[]
# # for item in seizure_timing_index:
# #     seizure_phase.append(var_trans_nomal[item])
# # SIvarshortseizure=sum(seizure_phase)/len(seizure_phase)
# # print(SIvarshortseizure)
# # var_phase=np.unwrap(np.angle(var_trans))
# # phase_whole_short=[]
# # for i in range(len(var_phase)):
# #     if var_phase[i]<0:
# #         phase_whole_short.append(var_phase[i] + abs((var_phase[i] // (2 * np.pi))) * (2 * np.pi))
# #     elif var_phase[i]>2*np.pi:
# #         phase_whole_short.append(var_phase[i] - (var_phase[i] // (2 * np.pi)) * (2 * np.pi))
# #     else:
# #         phase_whole_short.append(var_phase[i])
# #
# #
# # seizure_phase_var_long=[]
# # for item in seizure_timing_index:
# #     seizure_phase_var_long.append(phase_whole_long[item])
# # seizure_phase_var_short=[]
# # for item in seizure_timing_index:
# #     seizure_phase_var_short.append(phase_whole_short[item])
# # print(seizure_phase_var_long)
# # print(seizure_phase_var_short)
# #
# #
# # # ## histogram
# # bins_number = 18
# # bins = np.linspace(0, 2*np.pi, bins_number + 1)
# # n, _, _ = pyplot.hist(phase_whole_long, bins)
# # n1, _, _ = pyplot.hist(phase_whole_short, bins)
# # nsl, _, _ = pyplot.hist(seizure_phase_var_long, bins)
# # nss, _, _ = pyplot.hist(seizure_phase_var_short, bins)
# # pyplot.clf()
# # width = 2 * np.pi / bins_number
# # ax1 = pyplot.subplot(221, projection='polar')
# # ax1.bar(bins[:bins_number], n, width=width, bottom=0.0, alpha=0.2)
# # ax2 = pyplot.subplot(222, projection='polar')
# # ax2.bar(bins[:bins_number], nsl, width=width, bottom=0.0, alpha=0.9)
# # ax2.set_rlim(0,4)
# # ax3 = pyplot.subplot(223,  projection='polar')
# # ax3.bar(bins[:bins_number], n1, width=width, bottom=0.0, alpha=0.2)
# # ax4 = pyplot.subplot(224,  projection='polar')
# # ax4.bar(bins[:bins_number], nss, width=width, bottom=0.0, alpha=0.9)
# # ax4.set_rlim(0,4)
# # pyplot.savefig('hisvaroneday in SA 2')
# # # # ## see rising
# # ax1=pyplot.subplot(211)
# # ax1.set_ylabel('short cycle of RRI variance')
# # ax1.plot(t_modified,short_var_plot,'r',alpha=0.5)
# # ax1.annotate('',xy=(9.19205,np.max(short_var_plot)),xytext=(9.19205,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(24.16555,np.max(short_var_plot)),xytext=(24.16555,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(32.9738833,np.max(short_var_plot)),xytext=(32.9738833,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(45.149161,np.max(short_var_plot)),xytext=(45.149161,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(55.0694389,np.max(short_var_plot)),xytext=(55.0694389,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(85.90777,np.max(short_var_plot)),xytext=(85.90777,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(92.7538833,np.max(short_var_plot)),xytext=(92.7538833,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(104.916106,np.max(short_var_plot)),xytext=(104.916106,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(139.57055,np.max(short_var_plot)),xytext=(139.57055,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(152.573328,np.max(short_var_plot)),xytext=(152.573328,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# #
# #
# #
# #
# # ax2=pyplot.subplot(212)
# # ax2.set_ylabel('phase')
# # ax2.set_xlabel('time(hour)')
# # ax2.plot(t_modified,phase_whole_short)
# # pyplot.savefig('varsigonedayshort in SA 2')
# # pyplot.figure()
# # ax3=pyplot.subplot(211)
# # ax3.set_ylabel('long cycle of RRI variance')
# # ax3.plot(t_modified,long_rhythm_var_arr[0],'k')
# # ax3.annotate('',xy=(9.19205,np.max(long_rhythm_var_arr[0])),xytext=(9.19205,np.max(long_rhythm_var_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(24.16555,np.max(long_rhythm_var_arr[0])),xytext=(24.16555,np.max(long_rhythm_var_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(32.9738833,np.max(long_rhythm_var_arr[0])),xytext=(32.9738833,np.max(long_rhythm_var_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(45.149161,np.max(long_rhythm_var_arr[0])),xytext=(45.149161,np.max(long_rhythm_var_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(55.0694389,np.max(long_rhythm_var_arr[0])),xytext=(55.0694389,np.max(long_rhythm_var_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(85.90777,np.max(long_rhythm_var_arr[0])),xytext=(85.90777,np.max(long_rhythm_var_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(92.7538833,np.max(long_rhythm_var_arr[0])),xytext=(92.7538833,np.max(long_rhythm_var_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(104.916106,np.max(long_rhythm_var_arr[0])),xytext=(104.916106,np.max(long_rhythm_var_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(139.57055,np.max(long_rhythm_var_arr[0])),xytext=(139.57055,np.max(long_rhythm_var_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(152.573328,np.max(long_rhythm_var_arr[0])),xytext=(152.573328,np.max(long_rhythm_var_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax4=pyplot.subplot(212)
# # ax4.set_ylabel('phase')
# # ax4.set_xlabel('time(hour)')
# # ax4.plot(t_modified,phase_whole_long)
# # pyplot.savefig('varsigonedaylong in SA 2')
# #
# #
# #
# #
# # # ## calcualte cycles of autocorrelation
# # # smooth with one day
# # long_rhythm_value_arr=tools.smoother(value_arr, kernel='hamming',size=1440*2,mirror=True)
# # short_rhythm_value_arr_show=tools.smoother(value_arr, kernel='hamming',size=20,mirror=True)
# # short_rhythm_value_arr_show=short_rhythm_value_arr_show[0]
# # short_value_arr=np.array(value_arr)-np.array(long_rhythm_value_arr[0])
# # short_value_plot=tools.smoother(short_value_arr, kernel='hamming', size=20,mirror=True)
# # short_value_plot=short_value_plot[0]
# # pyplot.figure()
# # pyplot.plot(t_modified,value_arr,color=[0.5,0.5,0.5],label='raw autocorrelation')
# # pyplot.plot(t_modified,short_rhythm_value_arr_show,'r',alpha=0.5,label='short cycle')
# # pyplot.plot(t_modified,long_rhythm_value_arr[0],'k',label='long cycle')
# # pyplot.annotate('',xy=(9.19205,np.max(short_value_plot)),xytext=(9.19205,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(24.16555,np.max(short_value_plot)),xytext=(24.16555,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(32.9738833,np.max(short_value_plot)),xytext=(32.9738833,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(45.149161,np.max(short_value_plot)),xytext=(45.149161,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(55.0694389,np.max(short_value_plot)),xytext=(55.0694389,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(85.90777,np.max(short_value_plot)),xytext=(85.90777,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(92.7538833,np.max(short_value_plot)),xytext=(92.7538833,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(104.916106,np.max(short_value_plot)),xytext=(104.916106,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(139.57055,np.max(short_value_plot)),xytext=(139.57055,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.annotate('',xy=(152.573328,np.max(short_value_plot)),xytext=(152.573328,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
# # pyplot.xlabel('time(hour)')
# # pyplot.ylabel('autocorrelation')
# # pyplot.title('RRI autocorrelation in SA0124 (smoothing length is one day)')
# # pyplot.legend(loc='upper right')
# # pyplot.savefig('RRI autocorrelation in SA0124 2')
# #
# #
# # # # phase of autocorrelation
# # value_trans=hilbert(long_rhythm_value_arr[0])
# # value_trans_nomal=[]
# # for m in value_trans:
# #     value_trans_nomal.append(m/abs(m))
# #
# # SIvaluelong=sum(value_trans_nomal)/len(value_trans_nomal)
# # print(SIvaluelong)
# #
# # seizure_phase=[]
# # for item in seizure_timing_index:
# #     seizure_phase.append(value_trans_nomal[item])
# # SIvaluelongseizure=sum(seizure_phase)/len(seizure_phase)
# # print(SIvaluelongseizure)
# #
# # value_phase=np.unwrap(np.angle(value_trans))
# # phase_whole_value_long=[]
# # for i in range(len(value_phase)):
# #     if value_phase[i]<0:
# #         phase_whole_value_long.append(value_phase[i] + abs((value_phase[i] // (2 * np.pi))) * (2 * np.pi))
# #     elif value_phase[i]>2*np.pi:
# #         phase_whole_value_long.append(value_phase[i] - (value_phase[i] // (2 * np.pi)) * (2 * np.pi))
# #     else:
# #         phase_whole_value_long.append(value_phase[i])
# #
# # value_trans=hilbert(short_value_plot)
# # value_trans_nomal=[]
# # for m in value_trans:
# #     value_trans_nomal.append(m/abs(m))
# # SIvalueshort=sum(value_trans_nomal)/len(value_trans_nomal)
# # print(SIvalueshort)
# # seizure_phase=[]
# # for item in seizure_timing_index:
# #     seizure_phase.append(value_trans_nomal[item])
# # SIvalueshortseizure=sum(seizure_phase)/len(seizure_phase)
# # print(SIvalueshortseizure)
# # #
# # value_phase=np.unwrap(np.angle(value_trans))
# # phase_whole_value_short=[]
# # for i in range(len(value_phase)):
# #     if value_phase[i]<0:
# #         phase_whole_value_short.append(value_phase[i] + abs((value_phase[i] // (2 * np.pi))) * (2 * np.pi))
# #     elif value_phase[i]>2*np.pi:
# #         phase_whole_value_short.append(value_phase[i] - (value_phase[i] // (2 * np.pi)) * (2 * np.pi))
# #     else:
# #         phase_whole_value_short.append(value_phase[i])
# #
# # seizure_phase_value_long=[]
# # for item in seizure_timing_index:
# #     seizure_phase_value_long.append(phase_whole_value_long[item])
# # seizure_phase_value_short=[]
# # for item in seizure_timing_index:
# #     seizure_phase_value_short.append(phase_whole_value_short[item])
# # print(seizure_phase_value_long)
# # print(seizure_phase_value_short)
# # #
# # # # ## histogram
# # bins_number = 18
# # bins = np.linspace(0, 2*np.pi, bins_number + 1)
# # n, _, _ = pyplot.hist(phase_whole_value_long, bins)
# # n1, _, _ = pyplot.hist(phase_whole_value_short, bins)
# # nsl, _, _ = pyplot.hist(seizure_phase_value_long, bins)
# # nss, _, _ = pyplot.hist(seizure_phase_value_short, bins)
# # pyplot.clf()
# # width = 2 * np.pi / bins_number
# # ax1 = pyplot.subplot(221, projection='polar')
# # ax1.bar(bins[:bins_number], n, width=width, bottom=0.0, alpha=0.2)
# # ax2 = pyplot.subplot(222, projection='polar')
# # ax2.bar(bins[:bins_number], nsl, width=width, bottom=0.0, alpha=0.9)
# # ax2.set_rlim(0,4)
# # ax3 = pyplot.subplot(223,  projection='polar')
# # ax3.bar(bins[:bins_number], n1, width=width, bottom=0.0, alpha=0.2)
# # ax4 = pyplot.subplot(224,  projection='polar')
# # ax4.bar(bins[:bins_number], nss, width=width, bottom=0.0, alpha=0.9)
# # ax4.set_rlim(0,4)
# # pyplot.savefig('hisvalueoneday in SA 2')
# # ax1=pyplot.subplot(211)
# # ax1.set_ylabel('short cycle of autocorrelation')
# # ax1.plot(t_modified,short_value_plot,'r',alpha=0.5)
# # ax1.annotate('',xy=(9.19205,np.max(short_value_plot)),xytext=(9.19205,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(24.16555,np.max(short_value_plot)),xytext=(24.16555,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(32.9738833,np.max(short_value_plot)),xytext=(32.9738833,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(45.149161,np.max(short_value_plot)),xytext=(45.149161,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(55.0694389,np.max(short_value_plot)),xytext=(55.0694389,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(85.90777,np.max(short_value_plot)),xytext=(85.90777,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(92.7538833,np.max(short_value_plot)),xytext=(92.7538833,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(104.916106,np.max(short_value_plot)),xytext=(104.916106,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(139.57055,np.max(short_value_plot)),xytext=(139.57055,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax1.annotate('',xy=(152.573328,np.max(short_value_plot)),xytext=(152.573328,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# #
# #
# # ax2=pyplot.subplot(212)
# # ax2.set_ylabel('phase')
# # ax2.set_xlabel('time(hour)')
# # ax2.plot(t_modified,phase_whole_value_short)
# # pyplot.savefig('valuesigonedayshort in SA 2')
# # pyplot.figure()
# # ax3=pyplot.subplot(211)
# # ax3.set_ylabel('long cycle of autocorrelation')
# # ax3.plot(t_modified,long_rhythm_value_arr[0],'k')
# # ax3.annotate('',xy=(9.19205,np.max(long_rhythm_value_arr[0])),xytext=(9.19205,np.max(long_rhythm_value_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(24.16555,np.max(long_rhythm_value_arr[0])),xytext=(24.16555,np.max(long_rhythm_value_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(32.9738833,np.max(long_rhythm_value_arr[0])),xytext=(32.9738833,np.max(long_rhythm_value_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(45.149161,np.max(long_rhythm_value_arr[0])),xytext=(45.149161,np.max(long_rhythm_value_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(55.0694389,np.max(long_rhythm_value_arr[0])),xytext=(55.0694389,np.max(long_rhythm_value_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(85.90777,np.max(long_rhythm_value_arr[0])),xytext=(85.90777,np.max(long_rhythm_value_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(92.7538833,np.max(long_rhythm_value_arr[0])),xytext=(92.7538833,np.max(long_rhythm_value_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(104.916106,np.max(long_rhythm_value_arr[0])),xytext=(104.916106,np.max(long_rhythm_value_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(139.57055,np.max(long_rhythm_value_arr[0])),xytext=(139.57055,np.max(long_rhythm_value_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# # ax3.annotate('',xy=(152.573328,np.max(long_rhythm_value_arr[0])),xytext=(152.573328,np.max(long_rhythm_value_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# #
# # ax4=pyplot.subplot(212)
# # ax4.set_ylabel('phase')
# # ax4.set_xlabel('time(hour)')
# # ax4.plot(t_modified,phase_whole_value_long)
# # pyplot.savefig('valuesigonedaylong in SA 2')