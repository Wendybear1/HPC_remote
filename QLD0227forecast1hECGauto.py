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

from statsmodels.tsa.api import SARIMAX
# ###forecast EEG var

from statsmodels.tsa.api import SARIMAX
# ###forecast EEG var
csv_reader = pd.read_csv('/home/wxiong/seer_remote/ecg_data_result_PNES/RRI_ch21_rawauto_QLD0290_15s_3h.csv',sep=',',header=None)
Raw_variance_EEG= csv_reader.values
Raw_var_EEG_arr=[]
for item in Raw_variance_EEG:
    Raw_var_EEG_arr.append(float(item))



fore_arr_EEGvars=[]
save_data_EEGvars=[]
for k in range(27):
    var_arr=Raw_var_EEG_arr[0:(19450+240*3*k)]
    long_rhythm_var_arr=movingaverage(var_arr,240*6)

    long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(19450+240*3*k)]
    phase_short_EEGvar_arr=long_var_plot

    rolmean_short_EEGvar=phase_short_EEGvar_arr


    target_arr = []
    for i in range(450):
        target_arr.append(rolmean_short_EEGvar[i * 40])
    data = target_arr
    my_order = (1, 0, 1)
    my_seasonal_order = (1, 0, 1, 72)
    model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
    model_fit = model.fit()
    fore_arr_EEGvars.append(model_fit.predict(450, 467))
np.savetxt("newpar72p1d0q1_ch21_forecast81hsignal_3hcycle_RRIauto_QLD0290.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')



# csv_reader = pd.read_csv('/home/wxiong/seer_remote/ecg_data_result/1/RRI_ch31_rawvariance_NSW0352_15s_3h.csv', sep=',', header=None)
# Raw_variance_RRI31 = csv_reader.values
# csv_reader = pd.read_csv('/home/wxiong/seer_remote/ecg_data_result/1/RRI_ch31_rawauto_NSW0352_15s_3h.csv', sep=',', header=None)
# Raw_auto_RRI31 = csv_reader.values
#
# Raw_variance_RRI31_arr = []
# for item in Raw_variance_RRI31:
#     Raw_variance_RRI31_arr.append(float(item))
# Raw_auto_RRI31_arr = []
# for item in Raw_auto_RRI31:
#     Raw_auto_RRI31_arr.append(float(item))
#
# # t = np.linspace(2.9975, 2.9975 + 0.00416667 * (len(Raw_variance_RRI31_arr) - 1), len(Raw_variance_RRI31_arr))
#
#
#
# # fore_arr_RRIvars = []
# # for k in range(72):
# #     auto_arr = Raw_variance_RRI31_arr[(0 + 240 * k):(17800 + 240 * k)]
# #
# #     long_rhythm_var_arr = movingaverage(auto_arr, 240*6)
# #
# #     var_trans = hilbert(long_rhythm_var_arr)
# #     var_phase = np.angle(var_trans)
# #
# #     phase_short_RRIvar_arr = var_phase
# #
# #     # df_rolling=pd.DataFrame(np.array(phase_short_RRIvar_arr))
# #     # rolmean_short_RRIvar = df_rolling.rolling(480).mean()
# #     # rolmean_short_RRIvar=rolmean_short_RRIvar.values
# #
# #     rolmean_short_RRIvar = phase_short_RRIvar_arr[240*6:]
# #
# #     target_arr = []
# #     for i in range(433):
# #         target_arr.append(rolmean_short_RRIvar[i * 40])
# #
# #     data = target_arr
# #     my_order = (2, 1, 1)
# #     my_seasonal_order = (1, 1, 1, 72)
# #     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
# #     model_fit = model.fit()
# #     fore_arr_RRIvars.append(model_fit.predict(433, 439))
# # np.savetxt("forecast72h_1hraw_RRIvar_QLD0227.csv", fore_arr_RRIvars, delimiter=",", fmt='%s')
#
# fore_arr_RRIvars = []
# for k in range(27):
#     auto_arr = Raw_auto_RRI31_arr[0:(19450+240*3*k)]
#
#     long_rhythm_var_arr = movingaverage(auto_arr, 240 * 6)
#
#     # var_trans = hilbert(long_rhythm_var_arr)
#     # var_phase = np.angle(var_trans)
#     # phase_short_RRIvar_arr = var_phase
#
#     long_var_plot = long_rhythm_var_arr[(240 * 6 + 240 * 3 * k):(19450 + 240 * 3 * k)]
#     phase_short_RRIvar_arr = long_var_plot
#     rolmean_short_RRIvar = phase_short_RRIvar_arr
#
#
#     target_arr = []
#     for i in range(450):
#         target_arr.append(rolmean_short_RRIvar[i * 40])
#
#     data = target_arr
#     my_order = (1, 1, 1)
#     my_seasonal_order = (1, 1, 1, 144)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_RRIvars.append(model_fit.predict(450, 467))
# np.savetxt("forecast81hsignal_3hcycle_RRIauto_NSW0352.csv", fore_arr_RRIvars, delimiter=",", fmt='%s')







