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

def Rpeakfunction(signal, sampling_rate, show=True):
    if signal is None:
        raise TypeError("Please specify an input signal.")
    signal = np.array(signal)
    sampling_rate = float(sampling_rate)
    order = int(0.3 * sampling_rate)
    filtered, _, _ = st.filter_signal(signal=signal,ftype='FIR',band='bandpass',order=order,frequency=[3, 45],sampling_rate=sampling_rate)
    rpeaks, = hamilton_segmenter(signal=filtered, sampling_rate=sampling_rate)
    rpeaks, = correct_rpeaks(signal=filtered,rpeaks=rpeaks,sampling_rate=sampling_rate,tol=0.05)
    length = len(signal)
    T = (length - 1) / sampling_rate
    ts = np.linspace(0, T, length, endpoint=False)
    args = (ts, filtered, rpeaks)
    names = ('ts', 'filtered', 'rpeaks')
    return utils.ReturnTuple(args, names)

def correct_rpeaks(signal=None, rpeaks=None, sampling_rate=1000., tol=0.05):
    if signal is None:
        raise TypeError("Please specify an input signal.")
    if rpeaks is None:
        raise TypeError("Please specify the input R-peaks.")
    tol = int(tol * sampling_rate)
    length = len(signal)
    newR = []
    for r in rpeaks:
        a = r - tol
        if a < 0:
            continue
        b = r + tol
        if b > length:
            break
        newR.append(a + np.argmax(signal[a:b]))
    newR = sorted(list(set(newR)))
    newR = np.array(newR, dtype='int')

    return utils.ReturnTuple((newR,), ('rpeaks',))

def hamilton_segmenter(signal=None, sampling_rate=1000.):
    if signal is None:
        raise TypeError("Please specify an input signal.")
    sampling_rate = float(sampling_rate)
    length = len(signal)
    dur = length / sampling_rate
    v1s = int(1. * sampling_rate)
    v100ms = int(0.1 * sampling_rate)
    TH_elapsed = np.ceil(0.36 * sampling_rate)
    sm_size = int(0.08 * sampling_rate)
    init_ecg = 8
    if dur < init_ecg:
        init_ecg = int(dur)
    filtered, _, _ = st.filter_signal(signal=signal,ftype='butter',band='lowpass',order=4,frequency=25.,sampling_rate=sampling_rate)
    filtered, _, _ = st.filter_signal(signal=filtered,ftype='butter',band='highpass',order=4,frequency=3.,sampling_rate=sampling_rate)
    dx = np.abs(np.diff(filtered, 1) * sampling_rate)
    dx, _ = st.smoother(signal=dx, kernel='hamming', size=sm_size, mirror=True)
    qrspeakbuffer = np.zeros(init_ecg)
    noisepeakbuffer = np.zeros(init_ecg)
    peak_idx_test = np.zeros(init_ecg)
    noise_idx = np.zeros(init_ecg)
    rrinterval = sampling_rate * np.ones(init_ecg)
    a, b = 0, v1s
    all_peaks, _ = st.find_extrema(signal=dx, mode='max')
    for i in range(init_ecg):
        peaks, values = st.find_extrema(signal=dx[a:b], mode='max')
        try:
            ind = np.argmax(values)
        except ValueError:
            pass
        else:
            qrspeakbuffer[i] = values[ind]
            peak_idx_test[i] = peaks[ind] + a
        a += v1s
        b += v1s

    ANP = np.median(noisepeakbuffer)
    AQRSP = np.median(qrspeakbuffer)
    TH = 0.475
    DT = ANP + TH * (AQRSP - ANP)
    DT_vec = []
    indexqrs = 0
    indexnoise = 0
    indexrr = 0
    npeaks = 0
    offset = 0

    beats = []
    lim = int(np.ceil(0.2 * sampling_rate))
    diff_nr = int(np.ceil(0.045 * sampling_rate))
    bpsi, bpe = offset, 0

    for f in all_peaks:
        DT_vec += [DT]
        peak_cond = np.array((all_peaks > f - lim) * (all_peaks < f + lim) * (all_peaks != f))
        peaks_within = all_peaks[peak_cond]
        if peaks_within.any() and (max(dx[peaks_within]) > dx[f]):
            continue

        if dx[f] > DT:
            if f < diff_nr:
                diff_now = np.diff(signal[0:f + diff_nr])
            elif f + diff_nr >= len(signal):
                diff_now = np.diff(signal[f - diff_nr:len(dx)])
            else:
                diff_now = np.diff(signal[f - diff_nr:f + diff_nr])
            diff_signer = diff_now[diff_now > 0]
            if len(diff_signer) == 0 or len(diff_signer) == len(diff_now):
                continue

            if npeaks > 0:
                prev_rpeak = beats[npeaks - 1]
                elapsed = f - prev_rpeak
                if elapsed < TH_elapsed:
                    if prev_rpeak < diff_nr:
                        diff_prev = np.diff(signal[0:prev_rpeak + diff_nr])
                    elif prev_rpeak + diff_nr >= len(signal):
                        diff_prev = np.diff(signal[prev_rpeak - diff_nr:len(dx)])
                    else:
                        diff_prev = np.diff(signal[prev_rpeak - diff_nr:prev_rpeak + diff_nr])

                    slope_now = max(diff_now)
                    slope_prev = max(diff_prev)

                    if (slope_now < 0.5 * slope_prev):
                        continue
                if dx[f] < 3. * np.median(qrspeakbuffer):
                    beats += [int(f) + bpsi]
                else:
                    continue
                if bpe == 0:
                    rrinterval[indexrr] = beats[npeaks] - beats[npeaks - 1]
                    indexrr += 1
                    if indexrr == init_ecg:
                        indexrr = 0
                else:
                    if beats[npeaks] > beats[bpe - 1] + v100ms:
                        rrinterval[indexrr] = beats[npeaks] - beats[npeaks - 1]
                        indexrr += 1
                        if indexrr == init_ecg:
                            indexrr = 0

            elif dx[f] < 3. * np.median(qrspeakbuffer):
                beats += [int(f) + bpsi]
            else:
                continue

            npeaks += 1
            qrspeakbuffer[indexqrs] = dx[f]
            peak_idx_test[indexqrs] = f
            indexqrs += 1
            if indexqrs == init_ecg:
                indexqrs = 0
        if dx[f] <= DT:
            tf = f + bpsi
            RRM = np.median(rrinterval)
            if len(beats) >= 2:
                elapsed = tf - beats[npeaks - 1]
                if elapsed >= 1.5 * RRM and elapsed > TH_elapsed:
                    if dx[f] > 0.5 * DT:
                        beats += [int(f) + offset]
                        if npeaks > 0:
                            rrinterval[indexrr] = beats[npeaks] - beats[npeaks - 1]
                            indexrr += 1
                            if indexrr == init_ecg:
                                indexrr = 0
                        npeaks += 1
                        qrspeakbuffer[indexqrs] = dx[f]
                        peak_idx_test[indexqrs] = f
                        indexqrs += 1
                        if indexqrs == init_ecg:
                            indexqrs = 0
                else:
                    noisepeakbuffer[indexnoise] = dx[f]
                    noise_idx[indexnoise] = f
                    indexnoise += 1
                    if indexnoise == init_ecg:
                        indexnoise = 0
            else:
                noisepeakbuffer[indexnoise] = dx[f]
                noise_idx[indexnoise] = f
                indexnoise += 1
                if indexnoise == init_ecg:
                    indexnoise = 0

        ANP = np.median(noisepeakbuffer)
        AQRSP = np.median(qrspeakbuffer)
        DT = ANP + 0.475 * (AQRSP - ANP)

    beats = np.array(beats)
    r_beats = []
    thres_ch = 0.85
    adjacency = 0.05 * sampling_rate
    for i in beats:
        error = [False, False]
        if i - lim < 0:
            window = signal[0:i + lim]
            add = 0
        elif i + lim >= length:
            window = signal[i - lim:length]
            add = i - lim
        else:
            window = signal[i - lim:i + lim]
            add = i - lim

        w_peaks, _ = st.find_extrema(signal=window, mode='max')
        w_negpeaks, _ = st.find_extrema(signal=window, mode='min')
        zerdiffs = np.where(np.diff(window) == 0)[0]
        w_peaks = np.concatenate((w_peaks, zerdiffs))
        w_negpeaks = np.concatenate((w_negpeaks, zerdiffs))
        pospeaks = sorted(zip(window[w_peaks], w_peaks), reverse=True)
        negpeaks = sorted(zip(window[w_negpeaks], w_negpeaks))
        try:
            twopeaks = [pospeaks[0]]
        except IndexError:
            twopeaks = []
        try:
            twonegpeaks = [negpeaks[0]]
        except IndexError:
            twonegpeaks = []

        for i in range(len(pospeaks) - 1):
            if abs(pospeaks[0][1] - pospeaks[i + 1][1]) > adjacency:
                twopeaks.append(pospeaks[i + 1])
                break
        try:
            posdiv = abs(twopeaks[0][0] - twopeaks[1][0])
        except IndexError:
            error[0] = True

        for i in range(len(negpeaks) - 1):
            if abs(negpeaks[0][1] - negpeaks[i + 1][1]) > adjacency:
                twonegpeaks.append(negpeaks[i + 1])
                break
        try:
            negdiv = abs(twonegpeaks[0][0] - twonegpeaks[1][0])
        except IndexError:
            error[1] = True

        n_errors = sum(error)
        try:
            if not n_errors:
                if posdiv > thres_ch * negdiv:
                    r_beats.append(twopeaks[0][1] + add)
                else:
                    r_beats.append(twonegpeaks[0][1] + add)
            elif n_errors == 2:
                if abs(twopeaks[0][1]) > abs(twonegpeaks[0][1]):
                    r_beats.append(twopeaks[0][1] + add)
                else:
                    r_beats.append(twonegpeaks[0][1] + add)
            elif error[0]:
                r_beats.append(twopeaks[0][1] + add)
            else:
                r_beats.append(twonegpeaks[0][1] + add)
        except IndexError:
            continue

    rpeaks = sorted(list(set(r_beats)))
    rpeaks = np.array(rpeaks, dtype='int')
    return utils.ReturnTuple((rpeaks,), ('rpeaks',))




import os
channel_arr = []
value_arr=[]
variance_arr=[]
directory = r'/fred/oz132/Download/QLD0481'


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




# import os
# channel_arr = []
# value_arr=[]
# variance_arr=[]
# directory = r'/fred/oz132/SA0124/'
#
# target_signal_arr_ch1 = []
# target_signal_arr_ch2 = []
# target_signal_arr_ch3 = []
# for entry in os.scandir(directory):
#     if (entry.path.endswith("ECG.edf")
#             or entry.path.endswith("ECG.edf")) and entry.is_file():
#                 raw_ecg = mne.io.read_raw_edf(entry.path, preload=True)
#                 target_signal_1 = raw_ecg._data[0]
#                 target_signal_2 = raw_ecg._data[1]
#                 target_signal_3 = raw_ecg._data[2]
#                 target_signal_arr_ch1 = target_signal_arr_ch1 + list(target_signal_1)
#                 target_signal_arr_ch2 = target_signal_arr_ch2 + list(target_signal_2)
#                 target_signal_arr_ch3 = target_signal_arr_ch3 + list(target_signal_3)
# subtract_3_1 = np.array(target_signal_arr_ch3) - np.array(target_signal_arr_ch1)
# subtract_2_1 = np.array(target_signal_arr_ch2) - np.array(target_signal_arr_ch1)

signal = subtract_3_1
divsignal_arr = split(signal, 256 *5)
hr_31_arr = []
ts_31_arr=[]
for i in range(len(divsignal_arr)):
        target_signal_arr = divsignal_arr[i]
        r_peak = ecg.hamilton_segmenter(signal=target_signal_arr, sampling_rate=256)
        hr_31_arr.append(len(r_peak[0])*12)
        ts_31_arr.append(1579497060019.5312+5000*i)


# np.savetxt("hr_ts_ch31_vic2037_15s_3h.csv", ts_31_arr, delimiter=",", fmt='%s')
# np.savetxt("hr_ch31_timearr_vic2037_15s_3h.csv", hr_31_arr, delimiter=",", fmt='%s')

df = pd.DataFrame(data={"time": ts_31_arr, "hr": hr_31_arr})
df.to_csv("hr_ch31_QLD0481.csv", sep=',',index=False)




# signal = subtract_2_1
# divsignal_arr = split(signal, 256 * 15)
# hr_31_arr = []
# ts_31_arr=[]
# for i in range(len(divsignal_arr)):
#         target_signal_arr = divsignal_arr[i]
#         hr_ts_31, hr_31 = ecg.ecg(signal=target_signal_arr, sampling_rate=256, show=False)[5:7]
#         hr_31_arr.append(hr_31)
#         ts_31_arr.append(hr_ts_31+15*i)
#
#
# # np.savetxt("hr_ts_ch31_vic2037_15s_3h.csv", ts_31_arr, delimiter=",", fmt='%s')
# # np.savetxt("hr_ch31_timearr_vic2037_15s_3h.csv", hr_31_arr, delimiter=",", fmt='%s')
#
# df = pd.DataFrame(data={"time": ts_31_arr, "hr": hr_31_arr})
# df.to_csv("hr_ch21_SA0124./file.csv", sep=',',index=False)

