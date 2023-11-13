from __future__ import division
import mne
import numpy as np
import scipy.signal
from matplotlib import pyplot
import math
from scipy.fftpack import fft, ifft
from scipy import signal
from scipy.signal import hilbert
from scipy.signal import butter, lfilter, iirfilter,filtfilt
from biosppy.signals import tools

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
def Implement_Notch_Filter(fs, band, freq, ripple, order, filter_type, data):
    nyq = fs / 2.0
    low = freq - band / 2.0
    high = freq + band / 2.0
    low = low / nyq
    high = high / nyq
    b, a = iirfilter(order, [low, high], rp=ripple, btype='bandstop', analog=False, ftype=filter_type)
    filtered_data = filtfilt(b, a, data)
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
#
# directory =r'/fred/oz132/SA0124'
# for i in range(21):
#     channel_arr = []
#     dir_list = list(os.scandir(directory))
#     dir_list.sort(key=lambda d:d.path)
#     for entry in dir_list:
#         if (entry.path.endswith("EEG.edf")
#                 or entry.path.endswith("EEG.edf")) and entry.is_file():
#                     raw_eeg = mne.io.read_raw_edf(entry.path, preload=True)
#                     channel_arr = channel_arr + list(raw_eeg._data[i])
#                     channel_name=raw_eeg.ch_names[i]
#     ch_filtered = butter_bandpass_filter(channel_arr, 1, 30, 256, order=5)
#     ch_notch = Implement_Notch_Filter(256, 5, 50, 3, 5, 'butter', ch_filtered)
#
#     signal=ch_notch
#     divsignal_arr=split(signal,256*15)
#
#     target_signal_arr=[]
#     for i in range(len(divsignal_arr)):
#         target_signal_arr.append(divsignal_arr[i][0:256*15])
#
#     value_arr=[]
#     variance_arr=[]
#     value_lag_arr=[]
#     for k in range(len(target_signal_arr)):
#         x = target_signal_arr[k]
#         y = target_signal_arr[k] - target_signal_arr[k].mean()
#         target_signal_std = np.std(target_signal_arr[k])
#         target_signal_var=target_signal_std**2
#         variance_arr.append(target_signal_var)
#         y = y / target_signal_std
#         R = np.correlate(y, y, mode='full')/len(x)
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
#     np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/"+channel_name+"_EEGvariance_SA0124_15s_3h.csv", variance_arr, delimiter=",", fmt='%s')
#     np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/"+channel_name+"_EEGauto_SA0124_15s_3h.csv", value_arr, delimiter=",", fmt='%s')

# import pandas as pd
# import os
# channel_arr = []
# channel_arr_2 = []
# channel_arr_3 = []
# channel_arr_4 = []
# channel_arr_5 = []
# channel_arr_6 = []
# channel_arr_7 = []
# directory =r'/fred/oz132/DownloadEEG/VIC1027'
# # [F3, F4, P3 ,P4]
# dir_list = list(os.scandir(directory))
# dir_list.sort(key=lambda d:d.path)
# for entry in dir_list:
#     if (entry.path.endswith(".csv")) and entry.is_file():
#         raw_ecg = pd.read_csv(entry.path, skipinitialspace=True)
#         target_signal_1 = raw_ecg.O2
#         channel_arr = channel_arr + list(target_signal_1)
#         target_signal_1 = raw_ecg.O1
#         channel_arr_2 = channel_arr_2 + list(target_signal_1)
#         target_signal_1 = raw_ecg.F7
#         channel_arr_3 = channel_arr_3 + list(target_signal_1)
#         target_signal_1 = raw_ecg.F8
#         channel_arr_4 = channel_arr_4 + list(target_signal_1)
#         target_signal_1 = raw_ecg.T6
#         channel_arr_5 = channel_arr_5 + list(target_signal_1)
#         target_signal_1 = raw_ecg.T5
#         channel_arr_6 = channel_arr_6 + list(target_signal_1)
#         # target_signal_1 = raw_ecg.Fp2
#         # channel_arr_7 = channel_arr_7 + list(target_signal_1)
#
# ch_filtered = butter_bandpass_filter(channel_arr, 1, 30, 256, order=5)
# ch_notch = Implement_Notch_Filter(256, 5, 50, 3, 5, 'butter', ch_filtered)
# signal=ch_notch
# divsignal_arr=split(signal,256*15)
# target_signal_arr=[]
# for i in range(len(divsignal_arr)):
#     target_signal_arr.append(divsignal_arr[i][0:256*15])
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
# np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/O2_EEGvariance_VIC1027_15s_3h.csv", variance_arr, delimiter=",", fmt='%s')
# np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/O2_EEGauto_VIC1027_15s_3h.csv", value_arr, delimiter=",", fmt='%s')
# # np.savetxt("Cz_EEGauto_lag1_VIC0821_15s_3h.csv", value_arr, delimiter=",", fmt='%s')
#
# ch_filtered = butter_bandpass_filter(channel_arr_2, 1, 30, 256, order=5)
# ch_notch = Implement_Notch_Filter(256, 5, 50, 3, 5, 'butter', ch_filtered)
# signal=ch_notch
# divsignal_arr=split(signal,256*15)
# target_signal_arr=[]
# for i in range(len(divsignal_arr)):
#     target_signal_arr.append(divsignal_arr[i][0:256*15])
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
# np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/O1_EEGvariance_VIC1027_15s_3h.csv", variance_arr, delimiter=",", fmt='%s')
# np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/O1_EEGauto_VIC1027_15s_3h.csv", value_arr, delimiter=",", fmt='%s')
#
# ch_filtered = butter_bandpass_filter(channel_arr_3, 1, 30, 256, order=5)
# ch_notch = Implement_Notch_Filter(256, 5, 50, 3, 5, 'butter', ch_filtered)
# signal=ch_notch
# divsignal_arr=split(signal,256*15)
# target_signal_arr=[]
# for i in range(len(divsignal_arr)):
#     target_signal_arr.append(divsignal_arr[i][0:256*15])
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
# np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/F7_EEGvariance_VIC1027_15s_3h.csv", variance_arr, delimiter=",", fmt='%s')
# np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/F7_EEGauto_VIC1027_15s_3h.csv", value_arr, delimiter=",", fmt='%s')
# #
# ch_filtered = butter_bandpass_filter(channel_arr_4, 1, 30, 256, order=5)
# ch_notch = Implement_Notch_Filter(256, 5, 50, 3, 5, 'butter', ch_filtered)
# signal=ch_notch
# divsignal_arr=split(signal,256*15)
# target_signal_arr=[]
# for i in range(len(divsignal_arr)):
#     target_signal_arr.append(divsignal_arr[i][0:256*15])
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
# np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/F8_EEGvariance_VIC1027_15s_3h.csv", variance_arr, delimiter=",", fmt='%s')
# np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/F8_EEGauto_VIC1027_15s_3h.csv", value_arr, delimiter=",", fmt='%s')
#
#
# ch_filtered = butter_bandpass_filter(channel_arr_5, 1, 30, 256, order=5)
# ch_notch = Implement_Notch_Filter(256, 5, 50, 3, 5, 'butter', ch_filtered)
# signal=ch_notch
# divsignal_arr=split(signal,256*15)
# target_signal_arr=[]
# for i in range(len(divsignal_arr)):
#     target_signal_arr.append(divsignal_arr[i][0:256*15])
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
# np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/T6_EEGvariance_VIC1027_15s_3h.csv", variance_arr, delimiter=",", fmt='%s')
# np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/T6_EEGauto_VIC1027_15s_3h.csv", value_arr, delimiter=",", fmt='%s')
#
#
# ch_filtered = butter_bandpass_filter(channel_arr_6, 1, 30, 256, order=5)
# ch_notch = Implement_Notch_Filter(256, 5, 50, 3, 5, 'butter', ch_filtered)
# signal=ch_notch
# divsignal_arr=split(signal,256*15)
# target_signal_arr=[]
# for i in range(len(divsignal_arr)):
#     target_signal_arr.append(divsignal_arr[i][0:256*15])
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
# np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/T5_EEGvariance_VIC1027_15s_3h.csv", variance_arr, delimiter=",", fmt='%s')
# np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/T5_EEGauto_VIC1027_15s_3h.csv", value_arr, delimiter=",", fmt='%s')



# ch_filtered = butter_bandpass_filter(channel_arr_7, 1, 30, 256, order=5)
# ch_notch = Implement_Notch_Filter(256, 5, 50, 3, 5, 'butter', ch_filtered)
# signal=ch_notch
# divsignal_arr=split(signal,256*15)
# target_signal_arr=[]
# for i in range(len(divsignal_arr)):
#     target_signal_arr.append(divsignal_arr[i][0:256*15])
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
# np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/Fp2_EEGvariance_VIC2835_15s_3h.csv", variance_arr, delimiter=",", fmt='%s')
# np.savetxt("/home/wxiong/seer_remote/eeg_data_result/channels/Fp2_EEGauto_VIC2835_15s_3h.csv", value_arr, delimiter=",", fmt='%s')



# import pandas as pd
#
# import os
#
# data_pre=[]
# data_interictal=[]
# channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
# for m in range(len(channel)):
#     channel_arr = []
#     directory =r'/fred/oz132/DownloadEEG/VIC2835'
#     dir_list = list(os.scandir(directory))
#     dir_list.sort(key=lambda d:d.path)
#     for entry in dir_list:
#         if (entry.path.endswith(".csv")) and entry.is_file():
#             raw_ecg = pd.read_csv(entry.path, skipinitialspace=True)
#             ch=channel[m]
#             target_signal_1 = raw_ecg[ch]
#             channel_arr = channel_arr + list(target_signal_1)
#
#     index = [5468, 10332, 11682, 15941, 22516, 28271, 29126, 33686, 34127]  ## QLD0290
#     # index = [586, 6872, 10359, 16528, 33444, 34881, 36505, 38528]  ## VIC0829
#     # index = [1083,4491,5403,6715,8379,12191,13651,17035,18131,19667,24319,26047,31751,35043,35968] ## VIC0583
#     # index = [1701, 6781, 11290, 13475, 18450, 23500, 28619]  ## ACT0128
#     # index = [267, 998, 1193, 3252, 7014, 10660, 12255, 17875, 24345]  ## QLD1230
#     # index = [437, 1599, 4542, 5841, 7122, 10495, 10646, 11803, 13146, 16584,17723,22917,23367,23778,24583,28886,29797,33430,34921,35917] # QLD1282
#     # index = [1725, 6404, 7544, 11031, 12172, 13210, 16833, 18091, 23413, 24151, 24630, 30491, 35372,
#     #          36202, 36486]  ### vic2037
#     # index = [1520, 2818, 4366, 7590, 9973, 10516, 12303, 13670] ## VIC2835
#     # index = [2774, 7912, 13139, 16795, 22656, 26133] # SA1243
#     ## index = [1204, 6089, 11219, 28978, 31944]  ## VIC0821 edf
#
#
#     signal_select=[]
#     for j in range(len(index)):
#         # signal_select =signal_select+channel_arr[(index[j] * 15 * 256):(index[j] * 15 + 120) * 256]
#         signal_select = signal_select + channel_arr[(index[j] * 15 - 15 * 60) * 256:(index[j] * 15 * 256)]
#     data_pre.append(signal_select)
#
#     # signal_select_interictal = []
#     # for j in range(len(index)):
#     #     signal_select_interictal = signal_select_interictal + channel_arr[(index[j] * 15 - 75 * 60) * 256:(index[
#     #                                                                                                            j] * 15 - 15 * 60) * 256]
#     # data_interictal.append(signal_select)
#
# import pandas as pd
# df = pd.DataFrame()
# channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
# for i in range(len(data_pre)):
#     df[channel[i]]=data_pre[i]
#
# df.to_csv("/fred/oz132/EEG_ML/EEG_preictal_VIC2835.csv")
#
# # df = pd.DataFrame()
# # channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
# # for i in range(len(data_interictal)):
# #     df[channel[i]]=data_interictal[i]
# # df.to_csv("/fred/oz132/EEG_ML/EEG_interictal_VIC2835.csv")



import pandas as pd
import os

data_pre_15min = []
data_pre_30min = []
data_pre_45min = []
data_pre_60min = []
data_interictal = []
channel = ['Fz', 'C4', 'Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8',
           'T6', 'T5', 'Cz']
for m in range(len(channel)):
    channel_arr = []
    directory = r'/fred/oz132/DownloadEEG/ACT0128'
    dir_list = list(os.scandir(directory))
    dir_list.sort(key=lambda d: d.path)
    for entry in dir_list:
        if (entry.path.endswith(".csv")) and entry.is_file():
            raw_ecg = pd.read_csv(entry.path, skipinitialspace=True)
            ch = channel[m]
            target_signal_1 = raw_ecg[ch]
            channel_arr = channel_arr + list(target_signal_1)

    # index = [5468, 10332, 11682, 15941, 22516, 28271, 29126, 33686, 34127]  ## QLD0290
    # index = [586, 6872, 10359, 16528, 33444, 34881, 36505, 38528]  ## VIC0829
    # index = [1083,4491,5403,6715,8379,12191,13651,17035,18131,19667,24319,26047,31751,35043,35968] ## VIC0583
    index = [1701, 6781, 11290, 13475, 18450, 23500, 28619]  ## ACT0128
    # index = [267, 998, 1193, 3252, 7014, 10660, 12255, 17875, 24345]  ## QLD1230
    # index = [437, 1599, 4542, 5841, 7122, 10495, 10646, 11803, 13146, 16584,17723,22917,23367,23778,24583,28886,29797,33430,34921,35917] # QLD1282
    # index = [1725, 6404, 7544, 11031, 12172, 13210, 16833, 18091, 23413, 24151, 24630, 30491, 35372,
    #          36202, 36486]  ### vic2037
    # index = [1520, 2818, 4366, 7590, 9973, 10516, 12303, 13670] ## VIC2835
    # index = [2774, 7912, 13139, 16795, 22656, 26133] # SA1243 edf
    # index = [1204, 6089, 11219, 28978, 31944]  ## VIC0821

    signal_select = []
    for j in range(len(index)):
        # signal_select =signal_select+channel_arr[(index[j] * 15 * 256):(index[j] * 15 + 120) * 256]
        signal_select = signal_select + channel_arr[(index[j] * 15 - 15 * 60) * 256:(index[j] * 15 * 256)]
    data_pre_15min.append(signal_select)

    signal_select = []
    for j in range(len(index)):
        signal_select = signal_select + channel_arr[(index[j] * 15 - 30 * 60) * 256:(index[j] * 15 - 15 * 60) * 256]
    data_pre_30min.append(signal_select)

    signal_select = []
    for j in range(len(index)):
        signal_select = signal_select + channel_arr[(index[j] * 15 - 45 * 60) * 256:(index[j] * 15 - 30 * 60) * 256]
    data_pre_45min.append(signal_select)

    signal_select = []
    for j in range(len(index)):
        signal_select = signal_select + channel_arr[(index[j] * 15 - 60 * 60) * 256:(index[j] * 15 - 45 * 60) * 256]
    data_pre_60min.append(signal_select)

    # signal_select_interictal = []
    # for j in range(len(index)):
    #     signal_select_interictal = signal_select_interictal + channel_arr[(index[j] * 15 - 75 * 60) * 256:(index[
    #                                                                                                            j] * 15 - 15 * 60) * 256]
    # data_interictal.append(signal_select)

import pandas as pd

df = pd.DataFrame()
channel = ['Fz', 'C4', 'Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8',
           'T6', 'T5', 'Cz']
for i in range(len(data_pre_15min)):
    df[channel[i]] = data_pre_15min[i]
df.to_csv("/fred/oz132/EEG_ML/15minpreictal/EEG_preictal_ACT0128.csv")

for i in range(len(data_pre_30min)):
    df[channel[i]] = data_pre_30min[i]
df.to_csv("/fred/oz132/EEG_ML/30minpreictal/EEG_preictal_ACT0128.csv")

for i in range(len(data_pre_45min)):
    df[channel[i]] = data_pre_45min[i]
df.to_csv("/fred/oz132/EEG_ML/45minpreictal/EEG_preictal_ACT0128.csv")

for i in range(len(data_pre_60min)):
    df[channel[i]] = data_pre_60min[i]
df.to_csv("/fred/oz132/EEG_ML/60minpreictal/EEG_preictal_ACT0128.csv")




data_pre_15min = []
data_pre_30min = []
data_pre_45min = []
data_pre_60min = []
data_interictal = []
channel = ['Fz', 'C4', 'Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8',
           'T6', 'T5', 'Cz']
for m in range(len(channel)):
    channel_arr = []
    directory = r'/fred/oz132/DownloadEEG/QLD1230'
    dir_list = list(os.scandir(directory))
    dir_list.sort(key=lambda d: d.path)
    for entry in dir_list:
        if (entry.path.endswith(".csv")) and entry.is_file():
            raw_ecg = pd.read_csv(entry.path, skipinitialspace=True)
            ch = channel[m]
            target_signal_1 = raw_ecg[ch]
            channel_arr = channel_arr + list(target_signal_1)

    # index = [5468, 10332, 11682, 15941, 22516, 28271, 29126, 33686, 34127]  ## QLD0290
    # index = [586, 6872, 10359, 16528, 33444, 34881, 36505, 38528]  ## VIC0829
    # index = [1083,4491,5403,6715,8379,12191,13651,17035,18131,19667,24319,26047,31751,35043,35968] ## VIC0583
    # index = [1701, 6781, 11290, 13475, 18450, 23500, 28619]  ## ACT0128
    index = [267, 998, 1193, 3252, 7014, 10660, 12255, 17875, 24345]  ## QLD1230
    # index = [437, 1599, 4542, 5841, 7122, 10495, 10646, 11803, 13146, 16584,17723,22917,23367,23778,24583,28886,29797,33430,34921,35917] # QLD1282
    # index = [1725, 6404, 7544, 11031, 12172, 13210, 16833, 18091, 23413, 24151, 24630, 30491, 35372,
    #          36202, 36486]  ### vic2037
    # index = [1520, 2818, 4366, 7590, 9973, 10516, 12303, 13670] ## VIC2835
    # index = [2774, 7912, 13139, 16795, 22656, 26133] # SA1243 edf
    # index = [1204, 6089, 11219, 28978, 31944]  ## VIC0821

    signal_select = []
    for j in range(len(index)):
        # signal_select =signal_select+channel_arr[(index[j] * 15 * 256):(index[j] * 15 + 120) * 256]
        signal_select = signal_select + channel_arr[(index[j] * 15 - 15 * 60) * 256:(index[j] * 15 * 256)]
    data_pre_15min.append(signal_select)

    signal_select = []
    for j in range(len(index)):
        signal_select = signal_select + channel_arr[(index[j] * 15 - 30 * 60) * 256:(index[j] * 15 - 15 * 60) * 256]
    data_pre_30min.append(signal_select)

    signal_select = []
    for j in range(len(index)):
        signal_select = signal_select + channel_arr[(index[j] * 15 - 45 * 60) * 256:(index[j] * 15 - 30 * 60) * 256]
    data_pre_45min.append(signal_select)

    signal_select = []
    for j in range(len(index)):
        signal_select = signal_select + channel_arr[(index[j] * 15 - 60 * 60) * 256:(index[j] * 15 - 45 * 60) * 256]
    data_pre_60min.append(signal_select)

    # signal_select_interictal = []
    # for j in range(len(index)):
    #     signal_select_interictal = signal_select_interictal + channel_arr[(index[j] * 15 - 75 * 60) * 256:(index[
    #                                                                                                            j] * 15 - 15 * 60) * 256]
    # data_interictal.append(signal_select)

import pandas as pd

df = pd.DataFrame()
channel = ['Fz', 'C4', 'Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8',
           'T6', 'T5', 'Cz']
for i in range(len(data_pre_15min)):
    df[channel[i]] = data_pre_15min[i]
df.to_csv("/fred/oz132/EEG_ML/15minpreictal/EEG_preictal_QLD1230.csv")

for i in range(len(data_pre_30min)):
    df[channel[i]] = data_pre_30min[i]
df.to_csv("/fred/oz132/EEG_ML/30minpreictal/EEG_preictal_QLD1230.csv")

for i in range(len(data_pre_45min)):
    df[channel[i]] = data_pre_45min[i]
df.to_csv("/fred/oz132/EEG_ML/45minpreictal/EEG_preictal_QLD1230.csv")

for i in range(len(data_pre_60min)):
    df[channel[i]] = data_pre_60min[i]
df.to_csv("/fred/oz132/EEG_ML/60minpreictal/EEG_preictal_QLD1230.csv")











# import os
# directory =r'/fred/oz132/SA1243'
#
# data_pre=[]
# for i in range(21):
#     signal_channel = []
#     dir_list = list(os.scandir(directory))
#     dir_list.sort(key=lambda d:d.path)
#     channel_arr=[]
#     for entry in dir_list:
#         if (entry.path.endswith("EEG.edf")
#             or entry.path.endswith("EEG.edf")) and entry.is_file():
#                 raw_eeg = mne.io.read_raw_edf(entry.path, preload=True)
#                 target_signal = list(raw_eeg._data[i])
#                 channel_arr = channel_arr + target_signal
#
#
#     # index = [1487, 3829, 5081, 7195,10117, 12498, 15489, 18697, 21542, 24461, 27043, 29002, 29974]
#     # index = [966,6793,12505,18409,25580,29963,31460,35833]
#     # index = [10228, 14828, 17045, 18749, 26832]
#     # index = [437, 1599, 4542, 5841, 7122, 10495, 10646, 11803, 13146,
#     #          16584,17723,22917,23367,23778,24583,28886,29797,33430,34921,35917]
#     index = [2774, 7912, 13139, 16795, 22656, 26133]
#     signal_select=[]
#     for j in range(len(index)):
#         signal_select =signal_select+channel_arr[(index[j] * 15 * 256):(index[j] * 15 + 120) * 256]
#
#     data_pre.append(signal_select)
#
# import pandas as pd
# df = pd.DataFrame()
# channel=['Fz','C4','Pz', 'C3', 'F3', 'F4', 'P4', 'P3', 'A2', 'T4', 'A1', 'T3', 'Fp1', 'Fp2', 'O2', 'O1', 'F7', 'F8', 'T6', 'T5', 'Cz']
# for i in range(len(data_pre)):
#     df[channel[i]]=data_pre[i]
#
# df.to_csv("/home/wxiong/seer_remote/eeg_data_result/channels/EEGraw_SA1243.csv")