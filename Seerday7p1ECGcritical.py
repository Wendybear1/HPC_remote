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

def my_R_peaks(signal,sampling_rate):
    # check inputs
    if signal is None:
        raise TypeError("Please specify an input signal.")
    signal = np.array(signal)
    sampling_rate = float(sampling_rate)
    # filter signal
    order = int(0.3 * sampling_rate)
    filtered, _, _ = tools.filter_signal(signal=signal,ftype='FIR',band='bandpass',order=order,frequency=[3, 45],
                                      sampling_rate=sampling_rate)
    rpeaks, = ecg.hamilton_segmenter(signal=filtered, sampling_rate=sampling_rate)

    rpeaks, = ecg.correct_rpeaks(signal=filtered,rpeaks=rpeaks,sampling_rate=sampling_rate,tol=0.05)
    return rpeaks

def movingaverage(values, window_size):
    weights = (np.ones(window_size))/window_size
    a=np.ones(1)
    return lfilter(weights,a,values)

location = ["ecg_data_vic_0758/VIC0758 - 19.07.08 17.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.08 18.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.08 18.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.08 18.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.08 19.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.08 19.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.08 19.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.08 20.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.08 20.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.08 20.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.08 21.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.08 21.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.08 21.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.08 22.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.08 22.35.48 - ECG.edf", "ecg_data_vic_0758/VIC0758 - 19.07.08 22.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.08 23.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.08 23.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.08 23.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 00.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 00.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 00.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 01.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 01.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 01.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 02.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 02.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 02.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 03.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 03.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 03.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 04.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 04.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 04.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 05.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 05.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 05.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 06.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 06.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 06.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 07.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 07.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 07.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 08.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 08.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 08.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 09.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 09.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 09.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 10.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 10.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 10.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 11.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 11.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 11.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 12.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 12.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 12.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 13.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 13.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 13.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 14.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 14.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 14.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 15.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 15.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 15.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 16.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 16.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 16.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 17.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 17.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 17.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 18.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 18.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 18.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 19.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 19.35.48 - ECG.edf", "ecg_data_vic_0758/VIC0758 - 19.07.09 19.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 20.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 20.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 20.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 21.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 21.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 21.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 22.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 22.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 22.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.09 23.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 23.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.09 23.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 00.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 00.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 00.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 01.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 01.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 01.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 02.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 02.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 02.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 03.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 03.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 03.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 04.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 04.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 04.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 05.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 05.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 05.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 06.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 06.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 06.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 07.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 07.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 07.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 08.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 08.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 08.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 09.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 09.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 09.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 10.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 10.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 10.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 11.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 11.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 11.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 12.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 12.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 12.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 13.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 13.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 13.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 14.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 14.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 14.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 15.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 15.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 15.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 16.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 16.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 16.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 17.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 17.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 17.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 18.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 18.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 18.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 19.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 19.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 19.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 20.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 20.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 20.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 21.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 21.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 21.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 22.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 22.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 22.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.10 23.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 23.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.10 23.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 00.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 00.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 00.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 01.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 01.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 01.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 02.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 02.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 02.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 03.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 03.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 03.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 04.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 04.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 04.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 05.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 05.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 05.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 06.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 06.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 06.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 07.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 07.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 07.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 08.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 08.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 08.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 09.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 09.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 09.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 10.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 10.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 10.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 11.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 11.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 11.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 12.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 12.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 12.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 13.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 13.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 13.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 14.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 14.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 14.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 15.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 15.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 15.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 16.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 16.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 16.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 17.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 17.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 17.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 18.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 18.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 18.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 19.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 19.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 19.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 20.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 20.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 20.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 21.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 21.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 21.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 22.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 22.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 22.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.11 23.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 23.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.11 23.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 00.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 00.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 00.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 01.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 01.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 01.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 02.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 02.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 02.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 03.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 03.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 03.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 04.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 04.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 04.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 05.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 05.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 05.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 06.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 06.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 06.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 07.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 07.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 07.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 08.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 08.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 08.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 09.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 09.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 09.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 10.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 10.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 10.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 11.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 11.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 11.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 12.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 12.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 12.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 13.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 13.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 13.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 14.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 14.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 14.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 15.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 15.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 15.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 16.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 16.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 16.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 17.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 17.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 17.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 18.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 18.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 18.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 19.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 19.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 19.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 20.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 20.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 20.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 21.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 21.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 21.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 22.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 22.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 22.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.12 23.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 23.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.12 23.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 00.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 00.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 00.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 01.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 01.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 01.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 02.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 02.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 02.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 03.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 03.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 03.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 04.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 04.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 04.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 05.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 05.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 05.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 06.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 06.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 06.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 07.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 07.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 07.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 08.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 08.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 08.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 09.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 09.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 09.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 10.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 10.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 10.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 11.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 11.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 11.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 12.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 12.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 12.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 13.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 13.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 13.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 14.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 14.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 14.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 15.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 15.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 15.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 16.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 16.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 16.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 17.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 17.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 17.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 18.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 18.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 18.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 19.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 19.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 19.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 20.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 20.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 20.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 21.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 21.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 21.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 22.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 22.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 22.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.13 23.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 23.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.13 23.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 00.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 00.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 00.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 01.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 01.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 01.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 02.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 02.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 02.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 03.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 03.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 03.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 04.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 04.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 04.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 05.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 05.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 05.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 06.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 06.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 06.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 07.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 07.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 07.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 08.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 08.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 08.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 09.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 09.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 09.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 10.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 10.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 10.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 11.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 11.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 11.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 12.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 12.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 12.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 13.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 13.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 13.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 14.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 14.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 14.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 15.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 15.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 15.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 16.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 16.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 16.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 17.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 17.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 17.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 18.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 18.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 18.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 19.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 19.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 19.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 20.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 20.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 20.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 21.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 21.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 21.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 22.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 22.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 22.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.14 23.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 23.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.14 23.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.15 00.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 00.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 00.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.15 01.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 01.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 01.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.15 02.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 02.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 02.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.15 03.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 03.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 03.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.15 04.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 04.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 04.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.15 05.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 05.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 05.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.15 06.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 06.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 06.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.15 07.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 07.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 07.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.15 08.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 08.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 08.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.15 09.15.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 09.35.48 - ECG.edf","ecg_data_vic_0758/VIC0758 - 19.07.15 09.55.48 - ECG.edf",
            "ecg_data_vic_0758/VIC0758 - 19.07.15 10.15.48 - ECG.edf"]


print(len(location))
for j in range(1,2): ## channel2
    target_signal_arr = []
    for i in range(163):# start with VIC0758 - 19.07.08 17.55.48,end 07.20.23:55
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
    t_R_arr=[]
    for m in range(len(RRinter_arr_temp)):
        if RRinter_arr_temp[m] <= 1.5 and RRinter_arr_temp[m] >= 0.333:
            RRinter_arr.append(RRinter_arr_temp[m])
            t_R_arr.append(t_R_arr_temp[m + 1])



time_modified = []
for i in range(len(t_R_arr)):
    time_modified.append(2.99416+t_R_arr[i]/3600)

# print(len(time_modified))
# print(len(RRinter_arr))
# print(RRinter_arr)
# print(np.max(RRinter_arr))


# pyplot.plot(time_modified,RRinter_arr,'k')
# pyplot.annotate('',xy=(4.45416,np.max(RRinter_arr)),xytext=(4.45416,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# pyplot.annotate('',xy=(18.5086,np.max(RRinter_arr)),xytext=(18.5086,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# pyplot.annotate('',xy=(24.548,np.max(RRinter_arr)),xytext=(24.548,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# pyplot.annotate('',xy=(32.0750488,np.max(RRinter_arr)),xytext=(32.0750488,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# pyplot.annotate('',xy=(54.873,np.max(RRinter_arr)),xytext=(54.873,np.max(RRinter_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# pyplot.xlabel('time(h)')
# pyplot.ylabel('RRI rawsignal in VIC0758')
# pyplot.savefig('RRI rawsignal in VIC new')


Fs = 256
N = len(RRinter_arr)
dt = 1 / Fs
t = np.arange(0, N) * dt
p = np.polyfit(t, RRinter_arr, 1)
signal = np.array(RRinter_arr) - np.polyval(p, t)

divsignal_arr=split(signal,50) #50 RRI is about 0.5 min length
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
# #
# #
# # ## calculate cycles of vairance
# ## smoothing with one day, 1440 kernel filter
# # long_rhythm_var_arr=tools.smoother(variance_arr, kernel='hamming',size=1440*2,mirror=True)
# # short_rhythm_var_arr_show=tools.smoother(variance_arr, kernel='hamming',size=20,mirror=True)
# # short_rhythm_var_arr_show=short_rhythm_var_arr_show[0]
# # short_var_arr=np.array(variance_arr)-np.array(long_rhythm_var_arr[0])
# # short_var_plot=tools.smoother(short_var_arr, kernel='hamming', size=20,mirror=True)
# # short_var_plot=short_var_plot[0]
#
# print(variance_arr)
# print(value_arr)
#
# ## FIR filters
long_rhythm_var_arr=movingaverage(variance_arr,1440*2)
short_rhythm_var_arr_show=movingaverage(variance_arr,20)
short_var_arr=np.array(variance_arr)-np.array(long_rhythm_var_arr)
short_var_plot=movingaverage(short_var_arr,20)
# #
#
#
#
pyplot.figure()
t_modified=[]
for i in range(len(t_div_arr)):
    t_modified.append(t_div_arr[i][0])
#
seizure_timing_index=[]
for k in range(len(t_modified)):
    if t_modified[k]<4.45416 and t_modified[k+1]>=4.45416:
        seizure_timing_index.append(k)
    if t_modified[k]<18.5086 and t_modified[k+1]>=18.5086:
        seizure_timing_index.append(k)
    if t_modified[k]<24.548 and t_modified[k+1]>=24.548:
        seizure_timing_index.append(k)
    if t_modified[k]<32.0750488 and t_modified[k+1]>=32.0750488:
        seizure_timing_index.append(k)
    if t_modified[k]<54.873 and t_modified[k+1]>=54.873:
        seizure_timing_index.append(k)
print(seizure_timing_index)
#
# pyplot.plot(t_modified,variance_arr,color=[0.5,0.5,0.5],label='raw RRI variance')
# pyplot.plot(t_modified,short_rhythm_var_arr_show,'r',alpha=0.5,label='short cycle')
# pyplot.plot( t_modified,long_rhythm_var_arr,'k',label='long cycle')
# pyplot.legend(loc='upper right')
# pyplot.annotate('',xy=(4.45416,np.max(variance_arr)),xytext=(4.45416,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# pyplot.annotate('',xy=(18.5086,np.max(variance_arr)),xytext=(18.5086,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# pyplot.annotate('',xy=(24.548,np.max(variance_arr)),xytext=(24.548,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# pyplot.annotate('',xy=(32.0750488,np.max(variance_arr)),xytext=(32.0750488,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# pyplot.annotate('',xy=(54.873,np.max(variance_arr)),xytext=(54.873,np.max(variance_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# pyplot.xlabel('time(h)')
# pyplot.ylabel('variance')
# pyplot.title('RRI variance(smoothing length is one day)')
# pyplot.savefig('RRI variance in VIC')
# #
# #
# # # phase analysis
var_trans=hilbert(long_rhythm_var_arr)
# var_trans_nomal=[]
# for m in var_trans:
#     var_trans_nomal.append(m/abs(m))
# SIvarlong=sum(var_trans_nomal)/len(var_trans_nomal)
# print(SIvarlong)
# #
# seizure_phase=[]
# for item in seizure_timing_index:
#     seizure_phase.append(var_trans_nomal[item])
# SIvarlongseizure=sum(seizure_phase)/len(seizure_phase)
# print(SIvarlongseizure)
# #
var_phase=np.unwrap(np.angle(var_trans))
phase_whole_long=[]
for i in range(len(var_phase)):
    if var_phase[i]<0:
        phase_whole_long.append(var_phase[i] + abs((var_phase[i] // (2 * np.pi))) * (2 * np.pi))
    elif var_phase[i]>2*np.pi:
        phase_whole_long.append(var_phase[i] - (var_phase[i] // (2 * np.pi)) * (2 * np.pi))
    else:
        phase_whole_long.append(var_phase[i])


## channel ECG Ch2
provarl=[0,0.0015625,0,0,0.003333333,0,0,0,0,0,0,0,0,0,0,0.003891051,0.000667111,0.000944287]
bins_number = 18
bins = np.linspace(0, 2*np.pi, bins_number + 1)
pro_arr_long=[]
for i in range(len(phase_whole_long)):
    if phase_whole_long[i] > bins[1] and  phase_whole_long[i]<=bins[2]:
        pro_arr_long.append(0.0015625)
    elif phase_whole_long[i] > bins[4]  and phase_whole_long[i]<=bins[5]:
        pro_arr_long.append(0.003333333)
    elif  phase_whole_long[i] > bins[15] and phase_whole_long[i]<=bins[16]:
        pro_arr_long.append(0.003891051)
    elif phase_whole_long[i] > bins[16] and phase_whole_long[i]<= bins[17]:
        pro_arr_long.append(0.000667111)
    elif phase_whole_long[i] > bins[17]  and phase_whole_long[i]<= bins[18]:
        pro_arr_long.append(0.000944287)
    else:
        pro_arr_long.append(0)






var_trans=hilbert(short_var_plot)
# var_trans_nomal=[]
# for m in var_trans:
#     var_trans_nomal.append(m/abs(m))
# SIvarshort=sum(var_trans_nomal)/len(var_trans_nomal)
# print(SIvarshort)
# seizure_phase=[]
# for item in seizure_timing_index:
#     seizure_phase.append(var_trans_nomal[item])
# SIvarshortseizure=sum(seizure_phase)/len(seizure_phase)
# print(SIvarshortseizure)
# #
var_phase=np.unwrap(np.angle(var_trans))
phase_whole_short=[]
for i in range(len(var_phase)):
    if var_phase[i]<0:
        phase_whole_short.append(var_phase[i] + abs((var_phase[i] // (2 * np.pi))) * (2 * np.pi))
    elif var_phase[i]>2*np.pi:
        phase_whole_short.append(var_phase[i] - (var_phase[i] // (2 * np.pi)) * (2 * np.pi))
    else:
        phase_whole_short.append(var_phase[i])
# #


# #ch2
provars=[0,0,0,0,0,0,0.002421308,0,0,0,0,0,0,0.001666667,0.002941176,0.005181347,0,0.00621118]
bins_number = 18
bins = np.linspace(0, 2*np.pi, bins_number + 1)
pro_arr_short=[]
for i in range(len(phase_whole_short)):
    if phase_whole_short[i] > bins[6] and phase_whole_short[i]<=bins[7]:
        pro_arr_short.append(0.002421308)
    elif phase_whole_short[i] > bins[13] and phase_whole_short[i]<=bins[14]:
        pro_arr_short.append(0.001666667)
    elif phase_whole_short[i] > bins[14]and phase_whole_short[i]<=bins[15]:
        pro_arr_short.append(0.002941176)
    elif phase_whole_short[i] > bins[15] and phase_whole_short[i]<= bins[16]:
        pro_arr_short.append(0.005181347)
    elif phase_whole_short[i] > bins[17] and phase_whole_short[i]<= bins[18]:
        pro_arr_short.append(0.00621118)
    else:
        pro_arr_short.append(0)

whole_pro_arr=[]
for y in range(len(pro_arr_short)):
    whole_pro_arr.append(pro_arr_short[y]*pro_arr_long[y])
# print(whole_pro_arr)
print(np.max(whole_pro_arr))
a=[whole_pro_arr[143],whole_pro_arr[1500],whole_pro_arr[2106],whole_pro_arr[2961],whole_pro_arr[5330]]
print(a)


# seizure_phase_var_long=[]
# for item in seizure_timing_index:
#     seizure_phase_var_long.append(phase_whole_long[item])
# seizure_phase_var_short=[]
# for item in seizure_timing_index:
#     seizure_phase_var_short.append(phase_whole_short[item])
# print(seizure_phase_var_long)
# print(seizure_phase_var_short)
# #
# #
# # ## histogram
# bins_number = 18
# bins = np.linspace(0, 2*np.pi, bins_number + 1)
# n, _, _ = pyplot.hist(phase_whole_long, bins)
# n1, _, _ = pyplot.hist(phase_whole_short, bins)
# nsl, _, _ = pyplot.hist(seizure_phase_var_long, bins)
# nss, _, _ = pyplot.hist(seizure_phase_var_short, bins)
# print(n)
# print(n1)
# print(nsl)
# print(nss)
#
# pyplot.clf()
# width = 2 * np.pi / bins_number
# ax1 = pyplot.subplot(221, projection='polar')
# ax1.bar(bins[:bins_number], n, width=width, bottom=0.0, alpha=0.2)
# ax2 = pyplot.subplot(222, projection='polar')
# ax2.bar(bins[:bins_number], nsl, width=width, bottom=0.0, alpha=0.9)
# ax2.set_rlim(0,4)
# ax3 = pyplot.subplot(223,  projection='polar')
# ax3.bar(bins[:bins_number], n1, width=width, bottom=0.0, alpha=0.2)
# ax4 = pyplot.subplot(224,  projection='polar')
# ax4.bar(bins[:bins_number], nss, width=width, bottom=0.0, alpha=0.9)
# ax4.set_rlim(0,4)
# pyplot.savefig('hisvaroneday in VIC')
# # # ## see rising
# ax1=pyplot.subplot(211)
# ax1.set_ylabel('short cycle of RRIvariance')
# ax1.plot(t_modified,short_var_plot,'r',alpha=0.5)
# ax1.annotate('',xy=(4.45416,np.max(short_var_plot)),xytext=(4.45416,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax1.annotate('',xy=(18.5086,np.max(short_var_plot)),xytext=(18.5086,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax1.annotate('',xy=(24.548,np.max(short_var_plot)),xytext=(24.548,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax1.annotate('',xy=(32.0750488,np.max(short_var_plot)),xytext=(32.0750488,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax1.annotate('',xy=(54.873,np.max(short_var_plot)),xytext=(54.873,np.max(short_var_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax2=pyplot.subplot(212)
# ax2.set_ylabel('phase')
# ax2.set_xlabel('time(hour)')
# ax2.plot(t_modified,phase_whole_short)
# pyplot.savefig('varsigonedayshort in VIC')
# pyplot.figure()
# ax3=pyplot.subplot(211)
# ax3.set_ylabel('long cycle of RRI variance')
# ax3.plot(t_modified,long_rhythm_var_arr,'k')
# ax3.annotate('',xy=(4.45416,np.max(long_rhythm_var_arr)),xytext=(4.45416,np.max(long_rhythm_var_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax3.annotate('',xy=(18.5086,np.max(long_rhythm_var_arr)),xytext=(18.5086,np.max(long_rhythm_var_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax3.annotate('',xy=(24.548,np.max(long_rhythm_var_arr)),xytext=(24.548,np.max(long_rhythm_var_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax3.annotate('',xy=(32.0750488,np.max(long_rhythm_var_arr)),xytext=(32.0750488,np.max(long_rhythm_var_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax3.annotate('',xy=(54.873,np.max(long_rhythm_var_arr)),xytext=(54.873,np.max(long_rhythm_var_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax4=pyplot.subplot(212)
# ax4.set_ylabel('phase')
# ax4.set_xlabel('time(hour)')
# ax4.plot(t_modified,phase_whole_long)
# pyplot.savefig('varsigonedaylong in VIC')
# #
# #
# #
# #
# # ## calcualte cycles of autocorrelation
# # # smooth with one day
# # # long_rhythm_value_arr=tools.smoother(value_arr, kernel='hamming',size=1440*2,mirror=True)
# # # short_rhythm_value_arr_show=tools.smoother(value_arr, kernel='hamming',size=20,mirror=True)
# # # short_rhythm_value_arr_show=short_rhythm_value_arr_show[0]
# # # short_value_arr=np.array(value_arr)-np.array(long_rhythm_value_arr[0])
# # # short_value_plot=tools.smoother(short_value_arr, kernel='hamming', size=20,mirror=True)
# # # short_value_plot=short_value_plot[0]
long_rhythm_value_arr=movingaverage(value_arr,1440*2)
short_rhythm_value_arr_show=movingaverage(value_arr,20)
short_value_arr=np.array(value_arr)-np.array(long_rhythm_value_arr)
short_value_plot=movingaverage(short_value_arr,20)
#
#
# pyplot.figure()
# pyplot.plot(t_modified,value_arr,color=[0.5,0.5,0.5],label='raw autocorrelation')
# pyplot.plot(t_modified,short_rhythm_value_arr_show,'r',alpha=0.5,label='short cycle')
# pyplot.plot(t_modified,long_rhythm_value_arr,'k',label='long cycle')
# pyplot.annotate('',xy=(4.45416,np.max(short_value_plot)),xytext=(4.45416,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
# pyplot.annotate('',xy=(18.5086,np.max(short_value_plot)),xytext=(18.5086,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
# pyplot.annotate('',xy=(24.548,np.max(short_value_plot)),xytext=(24.548,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
# pyplot.annotate('',xy=(32.0750488,np.max(short_value_plot)),xytext=(32.0750488,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
# pyplot.annotate('',xy=(54.873,np.max(short_value_plot)),xytext=(54.873,np.max(short_value_plot)+0.1),arrowprops=dict(facecolor='black',shrink=0.05))
# pyplot.xlabel('time(hour)')
# pyplot.ylabel('autocorrelation')
# pyplot.title('RRI autocorrelation (smoothing length is one day)')
# pyplot.legend(loc='upper right')
# pyplot.savefig('RRI autocorrelation in VIC')
#
# #
# # # # phase of autocorrelation
value_trans=hilbert(long_rhythm_value_arr)
# value_trans_nomal=[]
# for m in value_trans:
#     value_trans_nomal.append(m/abs(m))
# SIvaluelong=sum(value_trans_nomal)/len(value_trans_nomal)
# print(SIvaluelong)
# seizure_phase=[]
# for item in seizure_timing_index:
#     seizure_phase.append(value_trans_nomal[item])
# SIvaluelongseizure=sum(seizure_phase)/len(seizure_phase)
# print(SIvaluelongseizure)
#
value_phase=np.unwrap(np.angle(value_trans))
phase_whole_value_long=[]
for i in range(len(value_phase)):
    if value_phase[i]<0:
        phase_whole_value_long.append(value_phase[i] + abs((value_phase[i] // (2 * np.pi))) * (2 * np.pi))
    elif value_phase[i]>2*np.pi:
        phase_whole_value_long.append(value_phase[i] - (value_phase[i] // (2 * np.pi)) * (2 * np.pi))
    else:
        phase_whole_value_long.append(value_phase[i])

### channel Ch2
proautol=[0,0.002673797,0,0,0.005263158,0,0,0,0,0,0,0,0,0,0,0,0.00120919,0.000704225]
bins_number = 18
bins = np.linspace(0, 2*np.pi, bins_number + 1)
pro_arr_long_auto=[]
for i in range(len(phase_whole_value_long)):
    if phase_whole_value_long[i]> bins[1] and phase_whole_value_long[i]<=bins[2]:
        pro_arr_long_auto.append(0.002673797)
    elif phase_whole_value_long[i]> bins[4] and phase_whole_value_long[i] <= bins[5]:
        pro_arr_long_auto.append(0.005263158)
    elif phase_whole_value_long[i]> bins[16] and phase_whole_value_long[i] <= bins[17]:
        pro_arr_long_auto.append(0.00120919)
    elif phase_whole_value_long[i]> bins[17] and phase_whole_value_long[i] <= bins[18]:
        pro_arr_long_auto.append(0.000704225)
    else:
        pro_arr_long_auto.append(0)




value_trans=hilbert(short_value_plot)
# value_trans_nomal=[]
# for m in value_trans:
#     value_trans_nomal.append(m/abs(m))
# SIvalueshort=sum(value_trans_nomal)/len(value_trans_nomal)
# print(SIvalueshort)
# seizure_phase=[]
# for item in seizure_timing_index:
#     seizure_phase.append(value_trans_nomal[item])
# SIvalueshortseizure=sum(seizure_phase)/len(seizure_phase)
# print(SIvalueshortseizure)
# #
value_phase=np.unwrap(np.angle(value_trans))
phase_whole_value_short=[]
for i in range(len(value_phase)):
    if value_phase[i]<0:
        phase_whole_value_short.append(value_phase[i] + abs((value_phase[i] // (2 * np.pi))) * (2 * np.pi))
    elif value_phase[i]>2*np.pi:
        phase_whole_value_short.append(value_phase[i] - (value_phase[i] // (2 * np.pi)) * (2 * np.pi))
    else:
        phase_whole_value_short.append(value_phase[i])
#
proautos=[0.002016129,0,0,0,0,0.004739336,0.006329114,0,0,0,0,0.006410256,0,0,0,0,0.002564103,0]
pro_arr_short_auto=[]
for i in range(len(phase_whole_value_short)):
    if phase_whole_value_short[i]>bins[0] and phase_whole_value_short[i]<=bins[1]:
        pro_arr_short_auto.append(0.002016129)
    elif phase_whole_value_short[i]> bins[5] and phase_whole_value_short[i] <=bins[6]:
        pro_arr_short_auto.append(0.004739336)
    elif phase_whole_value_short[i]>bins[6] and phase_whole_value_short[i] <=bins[7]:
        pro_arr_short_auto.append(0.006329114)
    elif phase_whole_value_short[i]> bins[11] and phase_whole_value_short[i] <= bins[12]:
        pro_arr_short_auto.append(0.006410256)
    elif phase_whole_value_short[i]> bins[16] and phase_whole_value_short[i] <= bins[17]:
        pro_arr_short_auto.append(0.002564103)
    else:
        pro_arr_short_auto.append(0)

whole_pro_arr_auto=[]
for m in range(len(pro_arr_short_auto)):
    whole_pro_arr_auto.append(pro_arr_short_auto[m]*pro_arr_long_auto[m])
# print(whole_pro_arr_auto)
print(np.max(whole_pro_arr_auto))
b=[whole_pro_arr_auto[143],whole_pro_arr_auto[1500],whole_pro_arr_auto[2106],whole_pro_arr_auto[2961],whole_pro_arr_auto[5330]]
print(b)



# seizure_phase_value_long=[]
# for item in seizure_timing_index:
#     seizure_phase_value_long.append(phase_whole_value_long[item])
# seizure_phase_value_short=[]
# for item in seizure_timing_index:
#     seizure_phase_value_short.append(phase_whole_value_short[item])
# print(seizure_phase_value_long)
# print(seizure_phase_value_short)
# #
# # ## histogram
# bins_number = 18
# bins = np.linspace(0, 2*np.pi, bins_number + 1)
# n, _, _ = pyplot.hist(phase_whole_value_long, bins)
# n1, _, _ = pyplot.hist(phase_whole_value_short, bins)
# nsl, _, _ = pyplot.hist(seizure_phase_value_long, bins)
# nss, _, _ = pyplot.hist(seizure_phase_value_short, bins)
# print(n)
# print(n1)
# print(nsl)
# print(nss)
# pyplot.clf()
# width = 2 * np.pi / bins_number
# ax1 = pyplot.subplot(221, projection='polar')
# ax1.bar(bins[:bins_number], n, width=width, bottom=0.0, alpha=0.2)
# ax2 = pyplot.subplot(222, projection='polar')
# ax2.bar(bins[:bins_number], nsl, width=width, bottom=0.0, alpha=0.9)
# ax2.set_rlim(0,4)
# ax3 = pyplot.subplot(223,  projection='polar')
# ax3.bar(bins[:bins_number], n1, width=width, bottom=0.0, alpha=0.2)
# ax4 = pyplot.subplot(224,  projection='polar')
# ax4.bar(bins[:bins_number], nss, width=width, bottom=0.0, alpha=0.9)
# ax4.set_rlim(0,4)
# pyplot.savefig('hisvalueonedayin VIC')
# ax1=pyplot.subplot(211)
# ax1.set_ylabel('short cycle of autocorrelation')
# ax1.plot(t_modified,short_value_plot,'r',alpha=0.5)
# ax1.annotate('',xy=(4.45416,np.max(short_value_plot)),xytext=(4.45416,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax1.annotate('',xy=(18.5086,np.max(short_value_plot)),xytext=(18.5086,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax1.annotate('',xy=(24.548,np.max(short_value_plot)),xytext=(24.548,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax1.annotate('',xy=(32.0750488,np.max(short_value_plot)),xytext=(32.0750488,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax1.annotate('',xy=(54.873,np.max(short_value_plot)),xytext=(54.873,np.max(short_value_plot)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax2=pyplot.subplot(212)
# ax2.set_ylabel('phase')
# ax2.set_xlabel('time(hour)')
# ax2.plot(t_modified,phase_whole_value_short)
# pyplot.savefig('valuesigonedayshort in VIC')
# pyplot.figure()
# ax3=pyplot.subplot(211)
# ax3.set_ylabel('long cycle of autocorrelation')
# ax3.plot(t_modified,long_rhythm_value_arr,'k')
# ax3.annotate('',xy=(4.45416,np.max(long_rhythm_value_arr)),xytext=(4.45416,np.max(long_rhythm_value_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax3.annotate('',xy=(18.5086,np.max(long_rhythm_value_arr)),xytext=(18.5086,np.max(long_rhythm_value_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax3.annotate('',xy=(24.548,np.max(long_rhythm_value_arr)),xytext=(24.548,np.max(long_rhythm_value_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax3.annotate('',xy=(32.0750488,np.max(long_rhythm_value_arr)),xytext=(32.0750488,np.max(long_rhythm_value_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax3.annotate('',xy=(54.873,np.max(long_rhythm_value_arr)),xytext=(54.873,np.max(long_rhythm_value_arr)+0.00000000001),arrowprops=dict(facecolor='black',shrink=0.05))
# ax4=pyplot.subplot(212)
# ax4.set_ylabel('phase')
# ax4.set_xlabel('time(hour)')
# ax4.plot(t_modified,phase_whole_value_long)
# pyplot.savefig('valuesigonedaylong in VIC')
#
# # #
# # print(seizure_timing_index)
#
#
#













