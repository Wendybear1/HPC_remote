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


# location = ["ecg_data_NSW0084a/NSW0084a - 19.03.07 15.53.42 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.07 15.54.43 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.07 16.12.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.07 16.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.07 16.52.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.07 17.12.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.07 17.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.07 17.52.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.07 18.12.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.07 18.32.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.07 18.52.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.07 19.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.07 19.32.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.07 19.52.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.07 20.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.07 20.32.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.07 20.52.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.07 21.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.07 21.32.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.07 21.52.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.07 22.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.07 22.32.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.07 22.52.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.07 23.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.07 23.32.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.07 23.52.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 00.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 00.32.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 00.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 01.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 01.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 01.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 02.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 02.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 02.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 03.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 03.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 03.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 04.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 04.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 04.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 05.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 05.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 05.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 06.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 06.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 06.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 07.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 07.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 07.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 08.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 08.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 08.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 09.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 09.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 09.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 10.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 10.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 10.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 11.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 11.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 11.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 12.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 12.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 12.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 13.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 13.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 13.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 14.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 14.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 14.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 15.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 15.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 15.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 16.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 16.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 16.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 17.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 17.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 17.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 18.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 18.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 18.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 19.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 19.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 19.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 20.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 20.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 20.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 21.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 21.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 21.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 22.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 22.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 22.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.08 23.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 23.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.08 23.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 00.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 00.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 00.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 01.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 01.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 01.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 02.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 02.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 02.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 03.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 03.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 03.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 04.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 04.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 04.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 05.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 05.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 05.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 06.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 06.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 06.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 07.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 07.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 07.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 08.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 08.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 08.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 09.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 09.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 09.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 10.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 10.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 10.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 11.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 11.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 11.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 12.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 12.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 12.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 13.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 13.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 13.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 14.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 14.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 14.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 15.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 15.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 15.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 16.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 16.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 16.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 17.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 17.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 17.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 18.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 18.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 18.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 19.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 19.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 19.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 20.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 20.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 20.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 21.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 21.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 21.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 22.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 22.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 22.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.09 23.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 23.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.09 23.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 00.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 00.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 00.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 01.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 01.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 01.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 02.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 02.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 02.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 03.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 03.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 03.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 04.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 04.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 04.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 05.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 05.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 05.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 06.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 06.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 06.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 07.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 07.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 07.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 08.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 08.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 08.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 09.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 09.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 09.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 10.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 10.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 10.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 11.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 11.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 11.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 12.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 12.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 12.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 13.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 13.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 13.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 14.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 14.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 14.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 15.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 15.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 15.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 16.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 16.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 16.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 17.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 17.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 17.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 18.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 18.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 18.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 19.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 19.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 19.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 20.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 20.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 20.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 21.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 21.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 21.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 22.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 22.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 22.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.10 23.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 23.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.10 23.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 00.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 00.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 00.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 01.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 01.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 01.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 02.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 02.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 02.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 03.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 03.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 03.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 04.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 04.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 04.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 05.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 05.32.23 - ECG.edf",
#
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 05.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 06.01.12 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 06.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 06.32.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 06.43.08 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 06.50.34 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 06.50.58 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 06.52.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 06.54.51 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 06.54.56 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 06.55.57 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 07.05.19 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 07.06.36 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 07.06.38 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 07.11.36 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 07.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 07.14.43 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 07.33.28 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 07.33.43 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 07.35.34 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 07.52.07 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 07.52.23 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 07.53.51 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 07.54.09 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 07.57.54 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 08.11.36 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 08.12.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 08.13.05 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 08.14.33 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 08.17.58 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 08.18.53 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 08.19.34 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 08.20.29 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 08.21.31 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 08.21.52 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 08.23.13 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 08.32.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 09.03.27 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 09.12.23 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 09.16.51 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 09.32.23 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 09.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 10.12.23 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 10.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 10.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 11.12.23 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 11.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 11.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 12.12.23 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 12.32.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 12.44.00 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 12.49.18 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 12.52.23 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 12.53.02 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 12.53.20 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 13.12.23 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 13.32.23 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 13.32.40 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 13.35.07 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 13.36.47 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 13.38.19 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 13.44.35 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 13.49.44 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 13.52.23 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 14.02.15 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 14.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 14.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 14.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 15.00.05 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 15.00.42 - ECG.edf",  "ecg_data_NSW0084a/NSW0084a - 19.03.11 15.09.02 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 15.09.48 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 15.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 15.12.53 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 15.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 15.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 16.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 16.32.44 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 16.47.24 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 16.52.23 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 17.07.08 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 17.07.42 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 17.08.03 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 17.08.28 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 17.09.32 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 17.11.02 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 17.12.23 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 17.21.10 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 17.21.53 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 17.32.23 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 17.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 18.12.23 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 18.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 18.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 19.00.50 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 19.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 19.16.43 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 19.19.09 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 19.19.48 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 19.19.59 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 19.20.11 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 19.20.15 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 19.32.39 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 19.36.51 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 19.55.13 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 19.59.04 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 20.01.21 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 20.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 20.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 20.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 21.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 21.32.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 21.36.19 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 21.38.19 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 21.42.39 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 21.44.22 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 21.46.11 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 21.47.24 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 21.48.02 - ECG.edf","ecg_data_NSW0084a/NSW0084a - 19.03.11 21.49.14 - ECG.edf",
#
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 21.52.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 22.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 22.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 22.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.11 23.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 23.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 23.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 00.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 00.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 00.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 01.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 01.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 01.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 02.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 02.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 02.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 03.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 03.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 03.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 04.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 04.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 04.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 05.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 05.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 05.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 06.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 06.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 06.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 07.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 07.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 07.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 08.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 08.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 08.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 09.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 09.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 09.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 10.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 10.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 10.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 11.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 11.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 11.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 12.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 12.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 12.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 13.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 13.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 13.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 14.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 14.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 14.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 15.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 15.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 15.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 16.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 16.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 16.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 17.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 17.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 17.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 18.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 18.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 18.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 19.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 19.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 19.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 20.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 20.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 20.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 21.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 21.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 21.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 22.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 22.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 22.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.12 23.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 23.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 23.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 00.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 00.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 00.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 01.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 01.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 01.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 02.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 02.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 02.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 03.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 03.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 03.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 04.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 04.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 04.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 05.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 05.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 05.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 06.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 06.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 06.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 07.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 07.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 07.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 08.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 08.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 08.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 09.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 09.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 09.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 10.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 10.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 10.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 11.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 11.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 11.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 12.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 12.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 12.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 13.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 13.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 13.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 14.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 14.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 14.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 15.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 15.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 15.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 16.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 16.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 16.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 17.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 17.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 17.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 18.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 18.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 18.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 19.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 19.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 19.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 20.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 20.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 20.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 21.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 21.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 21.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 22.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 22.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 22.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.13 23.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 23.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 23.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.14 00.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 00.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 00.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.14 01.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 01.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 01.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.14 02.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 02.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 02.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.14 03.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 03.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 03.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.14 04.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 04.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 04.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.14 05.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 05.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 05.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.14 06.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 06.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 06.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.14 07.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 07.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 07.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.14 08.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 08.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 08.52.23 - ECG.edf",
# "ecg_data_NSW0084a/NSW0084a - 19.03.14 09.12.23 - ECG.edf"]



location=["ecg_data_NSW0084a/NSW0084a - 19.03.11 21.52.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 22.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 22.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 22.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.11 23.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 23.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.11 23.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 00.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 00.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 00.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 01.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 01.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 01.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 02.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 02.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 02.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 03.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 03.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 03.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 04.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 04.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 04.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 05.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 05.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 05.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 06.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 06.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 06.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 07.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 07.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 07.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 08.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 08.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 08.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 09.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 09.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 09.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 10.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 10.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 10.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 11.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 11.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 11.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 12.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 12.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 12.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 13.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 13.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 13.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 14.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 14.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 14.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 15.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 15.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 15.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 16.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 16.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 16.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 17.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 17.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 17.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 18.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 18.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 18.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 19.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 19.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 19.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 20.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 20.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 20.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 21.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 21.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 21.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 22.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 22.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 22.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.12 23.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 23.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.12 23.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 00.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 00.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 00.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 01.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 01.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 01.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 02.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 02.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 02.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 03.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 03.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 03.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 04.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 04.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 04.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 05.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 05.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 05.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 06.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 06.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 06.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 07.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 07.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 07.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 08.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 08.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 08.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 09.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 09.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 09.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 10.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 10.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 10.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 11.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 11.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 11.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 12.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 12.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 12.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 13.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 13.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 13.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 14.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 14.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 14.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 15.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 15.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 15.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 16.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 16.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 16.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 17.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 17.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 17.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 18.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 18.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 18.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 19.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 19.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 19.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 20.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 20.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 20.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 21.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 21.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 21.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 22.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 22.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 22.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.13 23.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 23.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.13 23.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.14 00.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 00.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 00.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.14 01.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 01.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 01.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.14 02.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 02.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 02.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.14 03.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 03.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 03.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.14 04.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 04.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 04.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.14 05.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 05.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 05.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.14 06.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 06.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 06.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.14 07.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 07.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 07.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.14 08.12.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 08.32.23 - ECG.edf", "ecg_data_NSW0084a/NSW0084a - 19.03.14 08.52.23 - ECG.edf",
"ecg_data_NSW0084a/NSW0084a - 19.03.14 09.12.23 - ECG.edf"]





print(len(location))
for j in range(1):
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
    RRinter_arr=[]
    t_R_arr=[]
    for item in RRinter_arr_temp:
        if item <= 1.5 and item >= 0.333:
            t_index = RRinter_arr_temp.index(item)
            RRinter_arr.append(item)
            t_R_arr.append(t_R_arr_temp[t_index])


time_modified = []
for i in range(len(t_R_arr)):
    time_modified.append(101.978 + t_R_arr[i] / 3600)
pyplot.plot(time_modified,RRinter_arr,'k')
pyplot.annotate('',xy=(108.7955,np.max(RRinter_arr)),xytext=(108.7955,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
pyplot.annotate('',xy=(145.0874,np.max(RRinter_arr)),xytext=(145.0874,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))

pyplot.xlabel('time(h)')
pyplot.ylabel('RRI rawsignal in NSW')
pyplot.savefig('RRI rawsignal in NSW0084')

Fs = 256
N = len(RRinter_arr)
dt = 1 / Fs
t = np.arange(0, N) * dt
p = np.polyfit(t, RRinter_arr, 1)
signal = np.array(RRinter_arr) - np.polyval(p, t)

divsignal_arr=split(signal,50)
t_div_arr=split(time_modified,50)

target_signal_arr=[]
for i in range(len(divsignal_arr)):
    target_signal_arr.append(divsignal_arr[i][0:50])


value_arr=[]
variance_arr=[]
for k in range(len(target_signal_arr)):
    x = target_signal_arr[k]
    y = target_signal_arr[k] - target_signal_arr[k].mean()
    target_signal_std = np.std(target_signal_arr[k])
    target_signal_var=target_signal_std**2
    variance_arr.append(target_signal_var)
    y = y / target_signal_std
    R = np.correlate(y, y, mode='full')
    for k in range(len(R)):
        if R[k] < 0.5 * R.max():
            k = k + 1
        else:
            indice1 = k
            indice2 = len(R) - indice1
            value = indice2 - indice1
            value_arr.append(value)
            break


## calculate cycles of vairance
## smoothing with one day, 1440
long_rhythm_var_arr=tools.smoother(variance_arr, kernel='hamming',size=1440*2,mirror=True)
short_rhythm_var_arr_show=tools.smoother(variance_arr, kernel='hamming',size=20,mirror=True)
short_rhythm_var_arr_show=short_rhythm_var_arr_show[0]
short_var_arr=np.array(variance_arr)-np.array(long_rhythm_var_arr[0])
short_var_plot=tools.smoother(short_var_arr, kernel='hamming', size=20,mirror=True)
short_var_plot=short_var_plot[0]
# pyplot.figure()

t_modified=[]
for i in range(len(t_div_arr)):
    t_modified.append(t_div_arr[i][0])


seizure_timing_index=[]
for k in range(len(t_modified)):
    if t_modified[k]<108.7955 and t_modified[k+1]>=108.7955:
        seizure_timing_index.append(k)
    if t_modified[k]<145.0874 and t_modified[k+1]>=145.0874:
        seizure_timing_index.append(k)

print(seizure_timing_index)

pyplot.plot(t_modified,variance_arr,color=[0.5,0.5,0.5],label='raw RRI variance')
pyplot.plot(t_modified,short_rhythm_var_arr_show,'r',alpha=0.5,label='short cycle')
pyplot.plot( t_modified,long_rhythm_var_arr[0],'k',label='long cycle')
pyplot.legend(loc='upper right')
pyplot.annotate('',xy=(108.7955,np.max(variance_arr)),xytext=(108.7955,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
pyplot.annotate('',xy=(145.0874,np.max(variance_arr)),xytext=(145.0874,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
pyplot.xlabel('time(h)')
pyplot.ylabel('variance')
pyplot.title('RRI variance(smoothing length is one day)')
pyplot.savefig('RRI variance in NSW0098')

var_trans=hilbert(long_rhythm_var_arr[0])
var_trans_nomal=[]
for m in var_trans:
    var_trans_nomal.append(m/abs(m))
SIvarlong=sum(var_trans_nomal)/len(var_trans_nomal)
print(SIvarlong)

seizure_phase=[]
for item in seizure_timing_index:
    seizure_phase.append(var_trans_nomal[item])
SIvarlongseizure=sum(seizure_phase)/len(seizure_phase)
print(SIvarlongseizure)

var_phase=np.unwrap(np.angle(var_trans))
phase_whole_long=[]
for i in range(len(var_phase)):
    if var_phase[i]<0:
        phase_whole_long.append(var_phase[i] + abs((var_phase[i] // (2 * np.pi))) * (2 * np.pi))
    elif var_phase[i]>2*np.pi:
        phase_whole_long.append(var_phase[i] - (var_phase[i] // (2 * np.pi)) * (2 * np.pi))
    else:
        phase_whole_long.append(var_phase[i])

var_trans=hilbert(short_var_plot)
var_trans_nomal=[]
for m in var_trans:
    var_trans_nomal.append(m/abs(m))
SIvarshort=sum(var_trans_nomal)/len(var_trans_nomal)
print(SIvarshort)

seizure_phase=[]
for item in seizure_timing_index:
    seizure_phase.append(var_trans_nomal[item])
SIvarshortseizure=sum(seizure_phase)/len(seizure_phase)
print(SIvarshortseizure)

var_phase=np.unwrap(np.angle(var_trans))
phase_whole_short=[]
for i in range(len(var_phase)):
    if var_phase[i]<0:
        phase_whole_short.append(var_phase[i] + abs((var_phase[i] // (2 * np.pi))) * (2 * np.pi))
    elif var_phase[i]>2*np.pi:
        phase_whole_short.append(var_phase[i] - (var_phase[i] // (2 * np.pi)) * (2 * np.pi))
    else:
        phase_whole_short.append(var_phase[i])

seizure_phase_var_long=[]
for item in seizure_timing_index:
    seizure_phase_var_long.append(phase_whole_long[item])
seizure_phase_var_short=[]
for item in seizure_timing_index:
    seizure_phase_var_short.append(phase_whole_short[item])
print(seizure_phase_var_long)
print(seizure_phase_var_short)
## histogram
bins_number = 18
bins = np.linspace(0, 2*np.pi, bins_number + 1)
n, _, _ = pyplot.hist(phase_whole_long, bins)
n1, _, _ = pyplot.hist(phase_whole_short, bins)
nsl, _, _ = pyplot.hist(seizure_phase_var_long, bins)
nss, _, _ = pyplot.hist(seizure_phase_var_short, bins)
pyplot.clf()
width = 2 * np.pi / bins_number
ax1 = pyplot.subplot(221, projection='polar')
ax1.bar(bins[:bins_number], n, width=width, bottom=0.0, alpha=0.2)
ax2 = pyplot.subplot(222, projection='polar')
ax2.bar(bins[:bins_number], nsl, width=width, bottom=0.0, alpha=0.9)
ax2.set_rlim(0,4)
ax3 = pyplot.subplot(223,  projection='polar')
ax3.bar(bins[:bins_number], n1, width=width, bottom=0.0, alpha=0.2)
ax4 = pyplot.subplot(224,  projection='polar')
ax4.bar(bins[:bins_number], nss, width=width, bottom=0.0, alpha=0.9)
ax4.set_rlim(0,4)
pyplot.savefig('hisvaroneday in NSW0098')
# # ## see rising
ax1=pyplot.subplot(211)
ax1.set_ylabel('short cycle of RRIvariance')
ax1.plot(t_modified,short_var_plot,'r',alpha=0.5)
ax1.annotate('',xy=(108.7955,np.max(short_var_plot)),xytext=(108.7955,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
ax1.annotate('',xy=(145.0874,np.max(short_var_plot)),xytext=(145.0874,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
ax2=pyplot.subplot(212)
ax2.set_ylabel('phase')
ax2.set_xlabel('time(hour)')
ax2.plot(t_modified,phase_whole_short)
pyplot.savefig('varsigonedayshort in NSW0098')
pyplot.figure()
ax3=pyplot.subplot(211)
ax3.set_ylabel('long cycle of RRI variance')
ax3.plot(t_modified,long_rhythm_var_arr[0],'k')
ax3.annotate('',xy=(108.7955,np.max(long_rhythm_var_arr[0])),xytext=(108.7955,np.max(long_rhythm_var_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
ax3.annotate('',xy=(145.0874,np.max(long_rhythm_var_arr[0])),xytext=(145.0874,np.max(long_rhythm_var_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
ax4=pyplot.subplot(212)
ax4.set_ylabel('phase')
ax4.set_xlabel('time(hour)')
ax4.plot(t_modified,phase_whole_long)
pyplot.savefig('varsigonedaylong in NSW0098')




## calcualte cycles of autocorrelation
# smooth with one day
long_rhythm_value_arr=tools.smoother(value_arr, kernel='hamming',size=1440*2,mirror=True)
short_rhythm_value_arr_show=tools.smoother(value_arr, kernel='hamming',size=20,mirror=True)
short_rhythm_value_arr_show=short_rhythm_value_arr_show[0]
short_value_arr=np.array(value_arr)-np.array(long_rhythm_value_arr[0])
short_value_plot=tools.smoother(short_value_arr, kernel='hamming', size=20,mirror=True)
short_value_plot=short_value_plot[0]
pyplot.figure()
pyplot.plot(t_modified,value_arr,color=[0.5,0.5,0.5],label='raw autocorrelation')
pyplot.plot(t_modified,short_rhythm_value_arr_show,'r',alpha=0.5,label='short cycle')
pyplot.plot(t_modified,long_rhythm_value_arr[0],'k',label='long cycle')
pyplot.annotate('',xy=(108.7955,np.max(short_value_plot)),xytext=(108.7955,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
pyplot.annotate('',xy=(145.0874,np.max(short_value_plot)),xytext=(145.0874,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))

pyplot.xlabel('time(hour)')
pyplot.ylabel('autocorrelation')
pyplot.title('RRI autocorrelation (smoothing length is one day)')
pyplot.legend(loc='upper right')
pyplot.savefig('RRI autocorrelation in NSW0098')


# # phase of autocorrelation
value_trans=hilbert(long_rhythm_value_arr[0])
value_trans_nomal=[]
for m in value_trans:
    value_trans_nomal.append(m/abs(m))
SIvaluelong=sum(value_trans_nomal)/len(value_trans_nomal)
print(SIvaluelong)

seizure_phase=[]
for item in seizure_timing_index:
    seizure_phase.append(value_trans_nomal[item])
SIvaluelongseizure=sum(seizure_phase)/len(seizure_phase)
print(SIvaluelongseizure)

value_phase=np.unwrap(np.angle(value_trans))
phase_whole_value_long=[]
for i in range(len(value_phase)):
    if value_phase[i]<0:
        phase_whole_value_long.append(value_phase[i] + abs((value_phase[i] // (2 * np.pi))) * (2 * np.pi))
    elif value_phase[i]>2*np.pi:
        phase_whole_value_long.append(value_phase[i] - (value_phase[i] // (2 * np.pi)) * (2 * np.pi))
    else:
        phase_whole_value_long.append(value_phase[i])

value_trans=hilbert(short_value_plot)
value_trans_nomal=[]
for m in value_trans:
    value_trans_nomal.append(m/abs(m))
SIvalueshort=sum(value_trans_nomal)/len(value_trans_nomal)
print(SIvalueshort)
seizure_phase=[]
for item in seizure_timing_index:
    seizure_phase.append(value_trans_nomal[item])
SIvalueshortseizure=sum(seizure_phase)/len(seizure_phase)
print(SIvalueshortseizure)
#
value_phase=np.unwrap(np.angle(value_trans))
phase_whole_value_short=[]
for i in range(len(value_phase)):
    if value_phase[i]<0:
        phase_whole_value_short.append(value_phase[i] + abs((value_phase[i] // (2 * np.pi))) * (2 * np.pi))
    elif value_phase[i]>2*np.pi:
        phase_whole_value_short.append(value_phase[i] - (value_phase[i] // (2 * np.pi)) * (2 * np.pi))
    else:
        phase_whole_value_short.append(value_phase[i])

seizure_phase_value_long=[]
for item in seizure_timing_index:
    seizure_phase_value_long.append(phase_whole_value_long[item])
seizure_phase_value_short=[]
for item in seizure_timing_index:
    seizure_phase_value_short.append(phase_whole_value_short[item])
print(seizure_phase_value_long)
print(seizure_phase_value_short)
#
# ## histogram
bins_number = 18
bins = np.linspace(0, 2*np.pi, bins_number + 1)
n, _, _ = pyplot.hist(phase_whole_value_long, bins)
n1, _, _ = pyplot.hist(phase_whole_value_short, bins)
nsl, _, _ = pyplot.hist(seizure_phase_value_long, bins)
nss, _, _ = pyplot.hist(seizure_phase_value_short, bins)
pyplot.clf()
width = 2 * np.pi / bins_number
ax1 = pyplot.subplot(221, projection='polar')
ax1.bar(bins[:bins_number], n, width=width, bottom=0.0, alpha=0.2)
ax2 = pyplot.subplot(222, projection='polar')
ax2.bar(bins[:bins_number], nsl, width=width, bottom=0.0, alpha=0.9)
ax2.set_rlim(0,4)
ax3 = pyplot.subplot(223,  projection='polar')
ax3.bar(bins[:bins_number], n1, width=width, bottom=0.0, alpha=0.2)
ax4 = pyplot.subplot(224,  projection='polar')
ax4.bar(bins[:bins_number], nss, width=width, bottom=0.0, alpha=0.9)
ax4.set_rlim(0,4)
pyplot.savefig('hisvalueonedayin NSW')
ax1=pyplot.subplot(211)
ax1.set_ylabel('short cycle of autocorrelation')
ax1.plot(t_modified,short_value_plot,'r',alpha=0.5)
ax1.annotate('',xy=(108.7955,np.max(short_value_plot)),xytext=(108.7955,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
ax1.annotate('',xy=(145.0874,np.max(short_value_plot)),xytext=(145.0874,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))

ax2=pyplot.subplot(212)
ax2.set_ylabel('phase')
ax2.set_xlabel('time(hour)')
ax2.plot(t_modified,phase_whole_value_short)
pyplot.savefig('valuesigonedayshort in NSW0098')
pyplot.figure()
ax3=pyplot.subplot(211)
ax3.set_ylabel('long cycle of autocorrelation')
ax3.plot(t_modified,long_rhythm_value_arr[0],'k')
ax3.annotate('',xy=(108.7955,np.max(long_rhythm_value_arr[0])),xytext=(108.7955,np.max(long_rhythm_value_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
ax3.annotate('',xy=(145.0874,np.max(long_rhythm_value_arr[0])),xytext=(145.0874,np.max(long_rhythm_value_arr[0])+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))

ax4=pyplot.subplot(212)
ax4.set_ylabel('phase')
ax4.set_xlabel('time(hour)')
ax4.plot(t_modified,phase_whole_value_long)
pyplot.savefig('valuesigonedaylong in NSW0098')

