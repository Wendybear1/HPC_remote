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
csv_reader = pd.read_csv('/home/wxiong/seer_remote/eeg_data_result/Cz_EEGvariance_NSW0352_15s_3h.csv',sep=',',header=None)
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
save_data_EEGvars=[]
for k in range(27):
    var_arr=Raw_var_EEG_arr[0:(19450+240*3*k)]
    long_rhythm_var_arr=movingaverage(var_arr,240*6)
    long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(19450+240*3*k)]
    # long_var_plot = long_rhythm_var_arr[(240 * 24 + 240 * 3 * k):(19450 + 240 * 3 * k)]
    phase_short_EEGvar_arr=long_var_plot
    rolmean_short_EEGvar=phase_short_EEGvar_arr


    target_arr = []
    for i in range(450):
        target_arr.append(rolmean_short_EEGvar[i * 40])
    data = target_arr
    my_order = (1, 1, 1)
    my_seasonal_order = (1, 1, 1, 72)
    model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
    model_fit = model.fit()
    fore_arr_EEGvars.append(model_fit.predict(450, 467))
np.savetxt("Cz_forecast81hsignal_3hcycle_EEGvar_NSW0352_72.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')



#



