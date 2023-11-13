from __future__ import division
import mne
import numpy as np
import scipy.signal
from matplotlib import pyplot
import math
from scipy import signal
from scipy.signal import butter, lfilter,iirfilter
from scipy.signal import hilbert
from biosppy.signals import tools
import pandas as pd
from statsmodels.tsa.api import SARIMAX

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

# from statsmodels.tsa.api import SARIMAX
# ###forecast EEG var
# csv_reader = pd.read_csv('/home/wxiong/seer_remote/ecg_data_result_PNES/RRI_ch31_rawvariance_QLD1230_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(26):
#     var_arr=Raw_var_EEG_arr[0:(18720+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*24)
#
#     long_var_plot = long_rhythm_var_arr[(240*24+240*3*k):(18720+240*3*k)]
#     phase_short_EEGvar_arr=long_var_plot
#
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#
#     target_arr = []
#     for i in range(324):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 1, 1)
#     my_seasonal_order = (1, 1, 1, 144)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(324, 341))
# np.savetxt("cycles24h_ch31_forecast78hsignal_3hcycle_RRIvar_QLD1230.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


# from statsmodels.tsa.api import SARIMAX
# csv_reader = pd.read_csv('/home/wxiong/seer_remote/ecg_data_result_PNES/RRI_ch31_rawvariance_VIC0583_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(27):
#     var_arr=Raw_var_EEG_arr[0:(19450+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*24)
#     long_var_plot = long_rhythm_var_arr[(240*24+240*3*k):(19450+240*3*k)]
#
#
#     phase_short_EEGvar_arr=long_var_plot
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#     target_arr = []
#     for i in range(342):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 1, 1)
#     my_seasonal_order = (1, 1, 1, 72)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(342, 359))
# np.savetxt("cycles24h_ch31_forecast81hsignal_3hcycle_RRIvar_VIC0583.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


# from statsmodels.tsa.api import SARIMAX
# csv_reader = pd.read_csv('/home/wxiong/seer_remote/ecg_data_result_PNES/RRI_ch31_rawvariance_QLD1282_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(27):
#     var_arr=Raw_var_EEG_arr[0:(19450+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*1)
#     long_var_plot = long_rhythm_var_arr[(240*1+240*3*k):(19450+240*3*k)]
#     # var_trans=hilbert(long_var_plot)
#     # var_phase = np.angle(var_trans)
#
#     phase_short_EEGvar_arr=long_var_plot
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#     target_arr = []
#     for i in range(480):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 1, 1)
#     my_seasonal_order = (1, 1, 1, 144)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(480, 497))
# np.savetxt("cycles1h_ch31_forecast81hsignal_3hcycle_RRIvar_QLD1282.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


# from statsmodels.tsa.api import SARIMAX
# # ###forecast EEG var
# csv_reader = pd.read_csv('/home/wxiong/seer_remote/eeg_data_result/T3_EEGvariance_QLD0481_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
# var_arr=[]
# for item in Raw_var_EEG_arr:
#     if item<1e-8:
#         var_arr.append(item)
#     else:
#         var_arr.append(var_arr[-1])
# Raw_var_EEG_arr=var_arr
#
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(35):
#     var_arr=Raw_var_EEG_arr[0:(25202+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     # long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(25202+240*3*k)]
#     long_var_plot = long_rhythm_var_arr[(240 * 0 + 240 * 3 * k):(25202 + 240 * 3 * k)]
#     rolmean_short_EEGvar=long_var_plot
#
#
#     target_arr = []
#     for i in range(486):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 1, 1)
#     my_seasonal_order = (1, 1, 1, 144)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(486, 503))
# np.savetxt("T3_forecast93hsignal_3hcycle_EEGvar_QLD0481_0.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


# from statsmodels.tsa.api import SARIMAX
# csv_reader = pd.read_csv('/home/wxiong/seer_remote/ecg_data_result_PNES/RRI_ch31_rawvariance_VIC0821_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(23):
#     var_arr=Raw_var_EEG_arr[0:(16560+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(16560+240*3*k)]
#     # var_trans=hilbert(long_var_plot)
#     # var_phase = np.angle(var_trans)
#
#     phase_short_EEGvar_arr=long_var_plot
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#     target_arr = []
#     for i in range(378):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 1, 1)
#     my_seasonal_order = (1, 1, 1, 144)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(378, 395))
# np.savetxt("cycles6h_ch31_forecast69hsignal_3hcycle_RRIvar_VIC0821.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')



from statsmodels.tsa.api import SARIMAX

csv_reader = pd.read_csv('/fred/oz132/ECGresult/PNES/RRI_ch31_rawvariance_QLD3694_15s_3h.csv',sep=',',header=None)
Raw_variance_EEG= csv_reader.values
Raw_var_EEG_arr=[]
for item in Raw_variance_EEG:
    Raw_var_EEG_arr.append(float(item))

fore_arr_EEGvars=[]
save_data_EEGvars=[]
for k in range(20):
    var_arr=Raw_var_EEG_arr[0:(14400+240*3*k)]
    long_rhythm_var_arr=movingaverage(var_arr,240*12)
    long_var_plot = long_rhythm_var_arr[(240*12+240*3*k):(14400+240*3*k)]
    # var_trans=hilbert(long_var_plot)
    # var_phase = np.angle(var_trans)

    phase_short_EEGvar_arr=long_var_plot
    rolmean_short_EEGvar=phase_short_EEGvar_arr

    target_arr = []
    for i in range(288):
        target_arr.append(rolmean_short_EEGvar[i * 40])
    data = target_arr
    my_order = (1, 1, 1)
    my_seasonal_order = (1, 1, 1, 72)
    model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
    model_fit = model.fit()
    fore_arr_EEGvars.append(model_fit.predict(288, 305))
np.savetxt("cycles12hm72_ch31_forecast60hsignal_3hcycle_RRIvar_QLD3694_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')



# from statsmodels.tsa.api import SARIMAX
# csv_reader = pd.read_csv('/fred/oz132/ECGresult/PNES/RRI_ch31_rawvariance_WA0305_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(26):
#     var_arr=Raw_var_EEG_arr[0:(18720+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*12)
#     long_var_plot = long_rhythm_var_arr[(240*12+240*3*k):(18720+240*3*k)]
#     # var_trans=hilbert(long_var_plot)
#     # var_phase = np.angle(var_trans)
#
#     phase_short_EEGvar_arr=long_var_plot
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#     target_arr = []
#     for i in range(396):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 1, 1)
#     my_seasonal_order = (1, 1, 1, 360)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(396, 413))
# np.savetxt("cycles12hm360_ch31_forecast78hsignal_3hcycle_RRIvar_WA0305_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')