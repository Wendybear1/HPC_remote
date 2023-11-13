from __future__ import division
import mne
import numpy as np
import scipy.signal
from scipy.signal import butter, lfilter
import math
from scipy.fftpack import fft, ifft
from scipy import signal
from scipy.signal import butter, lfilter, iirfilter, filtfilt
from scipy.signal import hilbert
from biosppy.signals import tools
import pandas as pd
import csv
from biosppy.signals import ecg
from matplotlib import pyplot

from six.moves import range, zip

# 3rd party
import scipy.signal as ss

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

def Rpeakfunction(signal=None, sampling_rate=1000., show=True):
    # check inputs
    if signal is None:
        raise TypeError("Please specify an input signal.")
    # ensure numpy
    signal = np.array(signal)
    sampling_rate = float(sampling_rate)
    # filter signal
    order = int(0.3 * sampling_rate)
    filtered, _, _ = st.filter_signal(signal=signal,
                                      ftype='FIR',
                                      band='bandpass',
                                      order=order,
                                      frequency=[3, 45],
                                      sampling_rate=sampling_rate)

    # segment
    rpeaks, = hamilton_segmenter(signal=filtered, sampling_rate=sampling_rate)

    # correct R-peak locations
    rpeaks, = correct_rpeaks(signal=filtered,
                             rpeaks=rpeaks,
                             sampling_rate=sampling_rate,
                             tol=0.05)

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
    # check inputs
    if signal is None:
        raise TypeError("Please specify an input signal.")

    sampling_rate = float(sampling_rate)
    length = len(signal)
    dur = length / sampling_rate

    v1s = int(1. * sampling_rate)
    v100ms = int(0.1 * sampling_rate)
    TH_elapsed = np.ceil(0.36 * sampling_rate)
    sm_size = int(0.08 * sampling_rate)
    init_ecg = 8  # seconds for initialization
    if dur < init_ecg:
        init_ecg = int(dur)

    # filtering
    filtered, _, _ = st.filter_signal(signal=signal,
                                      ftype='butter',
                                      band='lowpass',
                                      order=4,
                                      frequency=25.,
                                      sampling_rate=sampling_rate)
    filtered, _, _ = st.filter_signal(signal=filtered,
                                      ftype='butter',
                                      band='highpass',
                                      order=4,
                                      frequency=3.,
                                      sampling_rate=sampling_rate)

    # diff
    dx = np.abs(np.diff(filtered, 1) * sampling_rate)

    # smoothing
    dx, _ = st.smoother(signal=dx, kernel='hamming', size=sm_size, mirror=True)

    # buffers
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
            # peak amplitude
            qrspeakbuffer[i] = values[ind]
            # peak location
            peak_idx_test[i] = peaks[ind] + a

        a += v1s
        b += v1s

    # thresholds
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

    # detection rules
    # 1 - ignore all peaks that precede or follow larger peaks by less than 200ms
    lim = int(np.ceil(0.2 * sampling_rate))
    diff_nr = int(np.ceil(0.045 * sampling_rate))
    bpsi, bpe = offset, 0

    for f in all_peaks:
        DT_vec += [DT]
        # 1 - Checking if f-peak is larger than any peak following or preceding it by less than 200 ms
        peak_cond = np.array((all_peaks > f - lim) * (all_peaks < f + lim) * (all_peaks != f))
        peaks_within = all_peaks[peak_cond]
        if peaks_within.any() and (max(dx[peaks_within]) > dx[f]):
            continue

        # 4 - If the peak is larger than the detection threshold call it a QRS complex, otherwise call it noise
        if dx[f] > DT:
            # 2 - look for both positive and negative slopes in raw signal
            if f < diff_nr:
                diff_now = np.diff(signal[0:f + diff_nr])
            elif f + diff_nr >= len(signal):
                diff_now = np.diff(signal[f - diff_nr:len(dx)])
            else:
                diff_now = np.diff(signal[f - diff_nr:f + diff_nr])
            diff_signer = diff_now[diff_now > 0]
            if len(diff_signer) == 0 or len(diff_signer) == len(diff_now):
                continue
            # RR INTERVALS
            if npeaks > 0:
                # 3 - in here we check point 3 of the Hamilton paper
                # that is, we check whether our current peak is a valid R-peak.
                prev_rpeak = beats[npeaks - 1]

                elapsed = f - prev_rpeak
                # if the previous peak was within 360 ms interval
                if elapsed < TH_elapsed:
                    # check current and previous slopes
                    if prev_rpeak < diff_nr:
                        diff_prev = np.diff(signal[0:prev_rpeak + diff_nr])
                    elif prev_rpeak + diff_nr >= len(signal):
                        diff_prev = np.diff(signal[prev_rpeak - diff_nr:len(dx)])
                    else:
                        diff_prev = np.diff(signal[prev_rpeak - diff_nr:prev_rpeak + diff_nr])

                    slope_now = max(diff_now)
                    slope_prev = max(diff_prev)

                    if (slope_now < 0.5 * slope_prev):
                        # if current slope is smaller than half the previous one, then it is a T-wave
                        continue
                if dx[f] < 3. * np.median(qrspeakbuffer):  # avoid retarded noise peaks
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
            # 4 - not valid
            # 5 - If no QRS has been detected within 1.5 R-to-R intervals,
            # there was a peak that was larger than half the detection threshold,
            # and the peak followed the preceding detection by at least 360 ms,
            # classify that peak as a QRS complex
            tf = f + bpsi
            # RR interval median
            RRM = np.median(rrinterval)  # initial values are good?

            if len(beats) >= 2:
                elapsed = tf - beats[npeaks - 1]

                if elapsed >= 1.5 * RRM and elapsed > TH_elapsed:
                    if dx[f] > 0.5 * DT:
                        beats += [int(f) + offset]
                        # RR INTERVALS
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

        # Update Detection Threshold
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
        # meanval = np.mean(window)
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

        # getting positive peaks
        for i in range(len(pospeaks) - 1):
            if abs(pospeaks[0][1] - pospeaks[i + 1][1]) > adjacency:
                twopeaks.append(pospeaks[i + 1])
                break
        try:
            posdiv = abs(twopeaks[0][0] - twopeaks[1][0])
        except IndexError:
            error[0] = True

        # getting negative peaks
        for i in range(len(negpeaks) - 1):
            if abs(negpeaks[0][1] - negpeaks[i + 1][1]) > adjacency:
                twonegpeaks.append(negpeaks[i + 1])
                break
        try:
            negdiv = abs(twonegpeaks[0][0] - twonegpeaks[1][0])
        except IndexError:
            error[1] = True

        # choosing type of R-peak
        n_errors = sum(error)
        try:
            if not n_errors:
                if posdiv > thres_ch * negdiv:
                    # pos noerr
                    r_beats.append(twopeaks[0][1] + add)
                else:
                    # neg noerr
                    r_beats.append(twonegpeaks[0][1] + add)
            elif n_errors == 2:
                if abs(twopeaks[0][1]) > abs(twonegpeaks[0][1]):
                    # pos allerr
                    r_beats.append(twopeaks[0][1] + add)
                else:
                    # neg allerr
                    r_beats.append(twonegpeaks[0][1] + add)
            elif error[0]:
                # pos poserr
                r_beats.append(twopeaks[0][1] + add)
            else:
                # neg negerr
                r_beats.append(twonegpeaks[0][1] + add)
        except IndexError:
            continue

    rpeaks = sorted(list(set(r_beats)))
    rpeaks = np.array(rpeaks, dtype='int')

    return utils.ReturnTuple((rpeaks,), ('rpeaks',))








# import os
# channel_arr = []
# value_arr=[]
# variance_arr=[]
# directory = r'/fred/oz132/Download/VIC0829'
#
#
# target_signal_arr_ch1 = []
# target_signal_arr_ch2 = []
# target_signal_arr_ch3 = []
# dir_list = list(os.scandir(directory))
# dir_list.sort(key=lambda d:d.path)
# for entry in dir_list:
#     if (entry.path.endswith(".csv")) and entry.is_file():
#         raw_ecg = pd.read_csv(entry.path, skipinitialspace=True)
#         target_signal_1 = raw_ecg.ECG1
#         target_signal_2 = raw_ecg.ECG2
#         target_signal_3 = raw_ecg.ECG3
#         target_signal_arr_ch1 = target_signal_arr_ch1 + list(target_signal_1)
#         target_signal_arr_ch2 = target_signal_arr_ch2 + list(target_signal_2)
#         target_signal_arr_ch3 = target_signal_arr_ch3 + list(target_signal_3)
#
# subtract_3_1 = np.array(target_signal_arr_ch3) - np.array(target_signal_arr_ch1)
# subtract_2_1 = np.array(target_signal_arr_ch2) - np.array(target_signal_arr_ch1)

# signal = subtract_3_1
# divsignal_arr = split(signal, 256 * 15)
# rpeaks_31_arr = []
# for i in range(len(divsignal_arr)):
#         target_signal_arr = divsignal_arr[i]
#         ts_31, filtered_31, rpeaks_31 = Rpeakfunction(signal=target_signal_arr, sampling_rate=256, show=False)
#         rpeaks_31_arr.append(rpeaks_31 + 256 * 15 * i)
#
# RRI_arr31_arr = [0]
# t_arr31 = []
# t_window_arr= []
# variance_arr = []
# value_arr =[]
# value_lag_arr=[]
# for item in rpeaks_31_arr:
#     RRI_arr31 = []
#     if len(item)==1 or len(item)==0:
#             RRI_arr31.append(RRI_arr31_arr[-1])
#             t_arr31.append(item / (256*3600))
#     else:
#         for j in range(len(item) - 1):
#             RRI_arr31.append((item[j + 1] - item[j]) / 256)
#             t_arr31.append(item[j + 1] / (256*3600))
#
#     RRI_arr31_modified=[]
#     for m in range(len(RRI_arr31)):
#         if RRI_arr31[m]<= 1.5 and RRI_arr31[m] >= 0.333:
#             RRI_arr31_modified.append(RRI_arr31[m])
#         else:
#             if m == 0:
#                 RRI_arr31_modified.append(RRI_arr31_arr[-1])
#                 m = m + 1
#             else:
#                 RRI_arr31_modified.append(RRI_arr31_modified[-1])
#                 m= m + 1
#     RRI_arr31_arr=RRI_arr31_arr+list(RRI_arr31_modified)
#
#     x = RRI_arr31_modified
#     y = RRI_arr31_modified - np.mean(RRI_arr31_modified)
#     target_signal_std = np.std(RRI_arr31_modified)
#     target_signal_var = target_signal_std ** 2
#     variance_arr.append(target_signal_var)
#     if target_signal_std==0:
#         value_arr.append(value_arr[-1])
#     else:
#         y = y / target_signal_std
#         y = y.flatten()
#         R = np.correlate(y, y, mode='full')/len(y)
#         for k in range(len(R)):
#             if R[k] < 0.5 * R.max():
#                 k = k + 1
#             else:
#                 indice1 = k
#                 indice2 = len(R) - indice1
#                 value = indice2 - indice1
#                 value_arr.append(value)
#                 break
#         for k in range(len(R)):
#             if R[k] == R.max():
#                 value_lag_arr.append(R[k+1])
#     if len(item)!=0:
#         t_window_arr.append(item[-1]/(256*3600))
#
#
# np.savetxt("rawRRI_ch31_VIC0829_15s_3h.csv", RRI_arr31_arr, delimiter=",", fmt='%s')
# np.savetxt("rawRRI_ch31_timearr_VIC0829_15s_3h.csv", t_arr31, delimiter=",", fmt='%s')
# np.savetxt("RRI_ch31_timewindowarr_VIC0829_15s_3h.csv", t_window_arr, delimiter=",", fmt='%s')
# np.savetxt("RRI_ch31_rawvariance_VIC0829_15s_3h.csv", variance_arr, delimiter=",", fmt='%s')
# np.savetxt("RRI_ch31_rawauto_VIC0829_15s_3h.csv", value_arr, delimiter=",", fmt='%s')
# np.savetxt("RRI_ch31_rawautolag1_VIC0829_15s_3h.csv", value_lag_arr, delimiter=",", fmt='%s')



# signal = subtract_2_1
# divsignal_arr = split(signal, 256 * 15)
# rpeaks_31_arr = []
# for i in range(len(divsignal_arr)):
#         target_signal_arr = divsignal_arr[i]
#         ts_31, filtered_31, rpeaks_31 = Rpeakfunction(signal=target_signal_arr, sampling_rate=256, show=False)
#         rpeaks_31_arr.append(rpeaks_31 + 256 * 15 * i)
#
# RRI_arr31_arr = [0]
# t_arr31 = []
# t_window_arr= []
# variance_arr = []
# value_arr =[]
# value_lag_arr=[]
# for item in rpeaks_31_arr:
#     RRI_arr31 = []
#     if len(item)==1 or len(item)==0:
#             RRI_arr31.append(RRI_arr31_arr[-1])
#             t_arr31.append(item / (256*3600))
#     else:
#         for j in range(len(item) - 1):
#             RRI_arr31.append((item[j + 1] - item[j]) / 256)
#             t_arr31.append(item[j + 1] / (256*3600))
#
#     RRI_arr31_modified=[]
#     for m in range(len(RRI_arr31)):
#         if RRI_arr31[m]<= 1.5 and RRI_arr31[m] >= 0.333:
#             RRI_arr31_modified.append(RRI_arr31[m])
#         else:
#             if m == 0:
#                 RRI_arr31_modified.append(RRI_arr31_arr[-1])
#                 m = m + 1
#             else:
#                 RRI_arr31_modified.append(RRI_arr31_modified[-1])
#                 m= m + 1
#     RRI_arr31_arr=RRI_arr31_arr+list(RRI_arr31_modified)
#
#     x = RRI_arr31_modified
#     y = RRI_arr31_modified - np.mean(RRI_arr31_modified)
#     target_signal_std = np.std(RRI_arr31_modified)
#     target_signal_var = target_signal_std ** 2
#     variance_arr.append(target_signal_var)
#     if target_signal_std==0:
#         value_arr.append(value_arr[-1])
#     else:
#         y = y / target_signal_std
#         y = y.flatten()
#         R = np.correlate(y, y, mode='full')/len(y)
#         for k in range(len(R)):
#             if R[k] < 0.5 * R.max():
#                 k = k + 1
#             else:
#                 indice1 = k
#                 indice2 = len(R) - indice1
#                 value = indice2 - indice1
#                 value_arr.append(value)
#                 break
#         for k in range(len(R)):
#             if R[k] == R.max():
#                 value_lag_arr.append(R[k+1])
#     if len(item)!=0:
#         t_window_arr.append(item[-1]/(256*3600))
#
#
# np.savetxt("rawRRI_ch21_VIC0829_15s_3h.csv", RRI_arr31_arr, delimiter=",", fmt='%s')
# np.savetxt("rawRRI_ch21_timearr_VIC0829_15s_3h.csv", t_arr31, delimiter=",", fmt='%s')
# np.savetxt("RRI_ch21_timewindowarr_VIC0829_15s_3h.csv", t_window_arr, delimiter=",", fmt='%s')
# np.savetxt("RRI_ch21_rawvariance_VIC0829_15s_3h.csv", variance_arr, delimiter=",", fmt='%s')
# np.savetxt("RRI_ch21_rawauto_VIC0829_15s_3h.csv", value_arr, delimiter=",", fmt='%s')
# np.savetxt("RRI_ch21_rawautolag1_VIC0829_15s_3h.csv", value_lag_arr, delimiter=",", fmt='%s')








import os
channel_arr = []
value_arr=[]
variance_arr=[]
directory = r'/fred/oz132/QLD2982'


target_signal_arr_ch1 = []
target_signal_arr_ch2 = []
target_signal_arr_ch3 = []
dir_list = list(os.scandir(directory))
dir_list.sort(key=lambda d:d.path)
for entry in dir_list:
    if (entry.path.endswith("ECG.edf")
            or entry.path.endswith("ECG.edf")) and entry.is_file():
                raw_ecg = mne.io.read_raw_edf(entry.path, preload=True)
                target_signal_1 = raw_ecg._data[0]
                target_signal_2 = raw_ecg._data[1]
                target_signal_3 = raw_ecg._data[2]
                target_signal_arr_ch1 = target_signal_arr_ch1 + list(target_signal_1)
                target_signal_arr_ch2 = target_signal_arr_ch2 + list(target_signal_2)
                target_signal_arr_ch3 = target_signal_arr_ch3 + list(target_signal_3)

subtract_3_1 = np.array(target_signal_arr_ch3) - np.array(target_signal_arr_ch1)
subtract_2_1 = np.array(target_signal_arr_ch2) - np.array(target_signal_arr_ch1)




signal = subtract_3_1
divsignal_arr = split(signal, 256 * 15)
rpeaks_31_arr = []
for i in range(len(divsignal_arr)):
        target_signal_arr = divsignal_arr[i]
        ts_31, filtered_31, rpeaks_31 = Rpeakfunction(signal=target_signal_arr, sampling_rate=256, show=False)
        rpeaks_31_arr.append(rpeaks_31 + 256 * 15 * i)


# # # ## calculate  RRI in channel3-1
RRI_arr31_arr = [0]
t_arr31 = []
t_window_arr= []
variance_arr = []
value_arr =[]
value_lag_arr=[]
for item in rpeaks_31_arr:
    RRI_arr31 = []
    if len(item)==1 or len(item)==0:
            RRI_arr31.append(RRI_arr31_arr[-1])
            t_arr31.append(item / (256*3600))
    else:
        for j in range(len(item) - 1):
            RRI_arr31.append((item[j + 1] - item[j]) / 256)
            t_arr31.append(item[j + 1] / (256*3600))
    # RRI_arr31_arr = RRI_arr31_arr + list(RRI_arr31)
    RRI_arr31_modified=[]
    for m in range(len(RRI_arr31)):
        if RRI_arr31[m]<= 1.5 and RRI_arr31[m] >= 0.333:
            RRI_arr31_modified.append(RRI_arr31[m])
        else:
            if m == 0:
                RRI_arr31_modified.append(RRI_arr31_arr[-1])
                m = m + 1
            else:
                RRI_arr31_modified.append(RRI_arr31_modified[-1])
                m= m + 1
    RRI_arr31_arr=RRI_arr31_arr+list(RRI_arr31_modified)

    x = RRI_arr31_modified
    y = RRI_arr31_modified - np.mean(RRI_arr31_modified)
    target_signal_std = np.std(RRI_arr31_modified)
    target_signal_var = target_signal_std ** 2
    variance_arr.append(target_signal_var)
    if target_signal_std==0:
        value_arr.append(value_arr[-1])
    else:
        y = y / target_signal_std
        y = y.flatten()
        R = np.correlate(y, y, mode='full')/len(y)
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
    if len(item)!=0:
        t_window_arr.append(item[-1]/(256*3600))


np.savetxt("rawRRI_ch31_QLD2982_15s_3h.csv", RRI_arr31_arr, delimiter=",", fmt='%s')
np.savetxt("rawRRI_ch31_timearr_QLD2982_15s_3h.csv", t_arr31, delimiter=",", fmt='%s')
np.savetxt("RRI_ch31_timewindowarr_QLD2982_15s_3h.csv", t_window_arr, delimiter=",", fmt='%s')
np.savetxt("RRI_ch31_rawvariance_QLD2982_15s_3h.csv", variance_arr, delimiter=",", fmt='%s')
np.savetxt("RRI_ch31_rawauto_QLD2982_15s_3h.csv", value_arr, delimiter=",", fmt='%s')
# np.savetxt("RRI_ch31_rawautolag1_QLD3694_15s_3h.csv", value_lag_arr, delimiter=",", fmt='%s')




# signal = subtract_2_1
# divsignal_arr = split(signal, 256 * 15)
# rpeaks_31_arr = []
# for i in range(len(divsignal_arr)):
#         target_signal_arr = divsignal_arr[i]
#         ts_31, filtered_31, rpeaks_31 = Rpeakfunction(signal=target_signal_arr, sampling_rate=256, show=False)
#         rpeaks_31_arr.append(rpeaks_31 + 256 * 15 * i)
#
#
# RRI_arr31_arr = [0]
# t_arr31 = []
# t_window_arr= []
# variance_arr = []
# value_arr =[]
# value_lag_arr=[]
# for item in rpeaks_31_arr:
#     RRI_arr31 = []
#     if len(item)==1 or len(item)==0:
#             RRI_arr31.append(RRI_arr31_arr[-1])
#             t_arr31.append(item / (256*3600))
#     else:
#         for j in range(len(item) - 1):
#             RRI_arr31.append((item[j + 1] - item[j]) / 256)
#             t_arr31.append(item[j + 1] / (256*3600))
#     # RRI_arr31_arr = RRI_arr31_arr + list(RRI_arr31)
#     RRI_arr31_modified=[]
#     for m in range(len(RRI_arr31)):
#         if RRI_arr31[m]<= 1.5 and RRI_arr31[m] >= 0.333:
#             RRI_arr31_modified.append(RRI_arr31[m])
#         else:
#             if m == 0:
#                 RRI_arr31_modified.append(RRI_arr31_arr[-1])
#                 m = m + 1
#             else:
#                 RRI_arr31_modified.append(RRI_arr31_modified[-1])
#                 m= m + 1
#     RRI_arr31_arr=RRI_arr31_arr+list(RRI_arr31_modified)
#
#     x = RRI_arr31_modified
#     y = RRI_arr31_modified - np.mean(RRI_arr31_modified)
#     target_signal_std = np.std(RRI_arr31_modified)
#     target_signal_var = target_signal_std ** 2
#     variance_arr.append(target_signal_var)
#     if target_signal_std==0:
#         value_arr.append(value_arr[-1])
#     else:
#         y = y / target_signal_std
#         y = y.flatten()
#         R = np.correlate(y, y, mode='full')/len(y)
#         for k in range(len(R)):
#             if R[k] < 0.5 * R.max():
#                 k = k + 1
#             else:
#                 indice1 = k
#                 indice2 = len(R) - indice1
#                 value = indice2 - indice1
#                 value_arr.append(value)
#                 break
#         for k in range(len(R)):
#             if R[k] == R.max():
#                 value_lag_arr.append(R[k+1])
#     if len(item)!=0:
#         t_window_arr.append(item[-1]/(256*3600))
#
#
# np.savetxt("rawRRI_ch21_QLD3694_15s_3h.csv", RRI_arr31_arr, delimiter=",", fmt='%s')
# np.savetxt("rawRRI_ch21_timearr_QLD3694_15s_3h.csv", t_arr31, delimiter=",", fmt='%s')
# np.savetxt("RRI_ch21_timewindowarr_QLD3694_15s_3h.csv", t_window_arr, delimiter=",", fmt='%s')
# np.savetxt("RRI_ch21_rawvariance_QLD3694_15s_3h.csv", variance_arr, delimiter=",", fmt='%s')
# np.savetxt("RRI_ch21_rawauto_QLD3694_15s_3h.csv", value_arr, delimiter=",", fmt='%s')
# # np.savetxt("RRI_ch21_rawautolag1_QLD3694_15s_3h.csv", value_lag_arr, delimiter=",", fmt='%s')

