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
# csv_reader = pd.read_csv('/home/wxiong/seer_remote/eeg_data_result/Cz_EEGvariance_VIC1006_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG[720:]:
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
# for k in range(27):
#     var_arr=Raw_var_EEG_arr[0:(19440+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#
#
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(19440+240*3*k)]
#     # var_trans=hilbert(long_var_plot)
#     # var_phase = np.angle(var_trans)
#
#     phase_short_EEGvar_arr=long_var_plot
#
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#
#     target_arr = []
#     for i in range(450):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 1, 1)
#     my_seasonal_order = (1, 1, 1, 144)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(450, 467))
# np.savetxt("forecast81hsignal_3hcycle_EEGvar_VIC1006_2.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')





# from statsmodels.tsa.api import SARIMAX
# # ### forecast EEG var
# csv_reader = pd.read_csv('/home/wxiong/seer_remote/eeg_data_result_PNES/Cz_EEGvariance_QLD1230_15s_3h.csv',sep=',',header=None)
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
# for k in range(26):
#     var_arr=Raw_var_EEG_arr[0:(18720+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*24)
#     long_var_plot = long_rhythm_var_arr[(240*24+240*3*k):(18720+240*3*k)]
#     rolmean_short_EEGvar=long_var_plot
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
# np.savetxt("cycles24h_Cz_forecast78hsignal_3hcycle_EEGvar_QLD1230.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')

from statsmodels.tsa.api import SARIMAX
# ### forecast EEG var
csv_reader = pd.read_csv('/fred/oz132/channels/PNES/channels/QLD0290_pure/Cz_EEGvariance_QLD0290_15s_3h.csv',sep=',',header=None)
Raw_variance_EEG= csv_reader.values
Raw_var_EEG_arr=[]
for item in Raw_variance_EEG:
    Raw_var_EEG_arr.append(float(item))

var_arr=[]
for item in Raw_var_EEG_arr:
    if item<1e-8:
        var_arr.append(item)
    else:
        var_arr.append(var_arr[-1])
Raw_var_EEG_arr=var_arr


fore_arr_EEGvars=[]
for k in range(27):
    var_arr=Raw_var_EEG_arr[0:(19450+240*3*k)]
    long_rhythm_var_arr=movingaverage(var_arr,240*6)
    long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(19450+240*3*k)]
    rolmean_short_EEGvar=long_var_plot


    target_arr = []
    for i in range(450):
        target_arr.append(rolmean_short_EEGvar[i * 40])
    data = target_arr
    my_order = (1, 1, 1)
    my_seasonal_order = (1, 1, 1, 144)
    model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
    model_fit = model.fit()
    fore_arr_EEGvars.append(model_fit.predict(450, 467))
np.savetxt("cycles6h_Cz_forecast81hsignal_3hcycle_EEGvar_QLD0290.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


# from statsmodels.tsa.api import SARIMAX
# csv_reader = pd.read_csv('/home/wxiong/seer_remote/eeg_data_result_PNES/Cz_EEGvariance_VIC0821_15s_3h.csv',sep=',',header=None)
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
# for k in range(23):
#     var_arr=Raw_var_EEG_arr[0:(16560+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(16560+240*3*k)]
#     rolmean_short_EEGvar=long_var_plot
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
# np.savetxt("cycles6h_Cz_forecast69hsignal_3hcycle_EEGvar_VIC0821.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


# from statsmodels.tsa.api import SARIMAX
# csv_reader = pd.read_csv('/fred/oz132/channels/PNES/channels/QLD3694_pure/Cz_EEGvariance_QLD3694_15s_3h.csv',sep=',',header=None)
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
# for k in range(20):
#     var_arr=Raw_var_EEG_arr[0:(14400+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*12)
#     long_var_plot = long_rhythm_var_arr[(240*12+240*3*k):(14400+240*3*k)]
#     rolmean_short_EEGvar=long_var_plot
#
#
#     target_arr = []
#     for i in range(288):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 1, 1)
#     my_seasonal_order = (1, 1, 1, 72)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(288, 305))
# np.savetxt("cycles12hm72_Cz_forecast60hsignal_3hcycle_EEGvar_QLD3694_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


# from statsmodels.tsa.api import SARIMAX
# csv_reader = pd.read_csv('/fred/oz132/channels/PNES/channels/QLD2982_pure/Cz_EEGvariance_QLD2982_15s_3h.csv',sep=',',header=None)
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
# for k in range(26):
#     var_arr=Raw_var_EEG_arr[0:(18720+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(18720+240*3*k)]
#     rolmean_short_EEGvar=long_var_plot
#
#     target_arr = []
#     for i in range(432):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 1, 1)
#     my_seasonal_order = (1, 1, 1, 432)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(432, 449))
# np.savetxt("cycles6hm432_Cz_forecast78hsignal_3hcycle_EEGvar_QLD2982_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')
