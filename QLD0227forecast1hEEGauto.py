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
###forecast EEG var
csv_reader = pd.read_csv('/home/wxiong/seer_remote/eeg_data_result/T3_EEGauto_SA0124_15s_3h.csv',sep=',',header=None)
Raw_variance_EEG= csv_reader.values
Raw_var_EEG_arr=[]
for item in Raw_variance_EEG:
    Raw_var_EEG_arr.append(float(item))



value_arr=[]
for item in Raw_var_EEG_arr:
    if item<500:
        value_arr.append(item)
    else:
        value_arr.append(value_arr[-1])
Raw_var_EEG_arr=value_arr


fore_arr_EEGvars=[]
save_data_EEGvars=[]
for k in range(27):
    var_arr=Raw_var_EEG_arr[0:(19624+240*3*k)]
    long_rhythm_var_arr=movingaverage(var_arr,240*6)
    long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(19624+240*3*k)]
    # var_trans=hilbert(long_var_plot)
    # var_phase = np.angle(var_trans)

    phase_short_EEGvar_arr=long_var_plot
    rolmean_short_EEGvar=phase_short_EEGvar_arr


    target_arr = []
    for i in range(454):
        target_arr.append(rolmean_short_EEGvar[i * 40])
    data = target_arr
    my_order = (1, 1, 1)
    my_seasonal_order = (1, 1, 1, 144)
    model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
    model_fit = model.fit()
    fore_arr_EEGvars.append(model_fit.predict(454, 471))
np.savetxt("T3_forecast81hsignal_3hcycle_EEGauto_SA0124.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')