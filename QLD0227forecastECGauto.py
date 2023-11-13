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
csv_reader = pd.read_csv('/fred/oz132/ECGresult/PNES/RRI_ch31_rawauto_QLD0290_15s_3h.csv',sep=',',header=None)
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
    my_order = (1, 1, 1)
    my_seasonal_order = (1, 1, 1, 144)
    model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
    model_fit = model.fit()
    fore_arr_EEGvars.append(model_fit.predict(450, 467))
np.savetxt("cycles6h_ch31_forecast81hsignal_3hcycle_RRIauto_QLD0290_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')




# from statsmodels.tsa.api import SARIMAX
# csv_reader = pd.read_csv('/home/wxiong/seer_remote/ecg_data_result_PNES/RRI_ch21_rawauto_VIC1012_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(25):
#     var_arr=Raw_var_EEG_arr[0:(18000+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(18000+240*3*k)]
#     # var_trans=hilbert(long_var_plot)
#     # var_phase = np.angle(var_trans)
#
#     phase_short_EEGvar_arr=long_var_plot
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#     target_arr = []
#     for i in range(414):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 1, 0)
#     my_seasonal_order = (1, 1, 0, 144)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(414, 431))
# np.savetxt("newpar144d1q0_ch21_forecast75hsignal_3hcycle_RRIauto_VIC1012.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')



# from statsmodels.tsa.api import SARIMAX
# csv_reader = pd.read_csv('/home/wxiong/seer_remote/ecg_data_result_PNES/RRI_ch31_rawauto_VIC0821_15s_3h.csv',sep=',',header=None)
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
# np.savetxt("cycles6h_ch31_forecast69hsignal_3hcycle_RRIauto_VIC0821.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


# from statsmodels.tsa.api import SARIMAX
# csv_reader = pd.read_csv('/fred/oz132/ECGresult/PNES/RRI_ch31_rawauto_QLD3694_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(20):
#     var_arr=Raw_var_EEG_arr[0:(14400+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*12)
#     long_var_plot = long_rhythm_var_arr[(240*12+240*3*k):(14400+240*3*k)]
#     # var_trans=hilbert(long_var_plot)
#     # var_phase = np.angle(var_trans)
#
#     phase_short_EEGvar_arr=long_var_plot
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
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
# np.savetxt("cycles12hm72_ch31_forecast60hsignal_3hcycle_RRIauto_QLD3694_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


# csv_reader = pd.read_csv('/fred/oz132/seer_remote/ecg_data_result_PNES/RRI_ch31_rawauto_ACT0128_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(24):
#     var_arr=Raw_var_EEG_arr[0:(17280+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(17280+240*3*k)]
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
#     my_order = (1, 0, 1)
#     my_seasonal_order = (1, 0, 1, 216)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(396, 413))
# np.savetxt("cycles6hd0m216_ch31_forecast72hsignal_3hcycle_RRIauto_ACT0128_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


# from statsmodels.tsa.api import SARIMAX
# csv_reader = pd.read_csv('/fred/oz132/ECGresult/PNES/RRI_ch31_rawauto_WA0305_15s_3h.csv',sep=',',header=None)
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
#     my_seasonal_order = (1, 1, 1, 288)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(396, 413))
# np.savetxt("cycles12hm288_ch31_forecast78hsignal_3hcycle_RRIauto_WA0305_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')
