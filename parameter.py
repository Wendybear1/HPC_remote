from __future__ import division
from math import sqrt
from multiprocessing import cpu_count
from joblib import Parallel
from joblib import delayed
from warnings import catch_warnings
from warnings import filterwarnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error

import numpy as np
import scipy.signal
from scipy.signal import butter, lfilter
from matplotlib import pyplot
import math
from scipy.fftpack import fft, ifft
import pandas as pd
from scipy.signal import butter, lfilter,iirfilter
from scipy.signal import hilbert
from biosppy.signals import tools
from scipy import signal
import statsmodels
from statsmodels.tsa.stattools import adfuller


# one-step sarima forecast
def sarima_forecast(history, config):
    order, sorder, trend = config
    # define model
    model = SARIMAX(history, order=order, seasonal_order=sorder, trend=trend, enforce_stationarity=False,
                    enforce_invertibility=False)
    # fit model
    model_fit = model.fit(disp=False)
    # make one step forecast
    yhat = model_fit.predict(len(history), len(history))
    return yhat[0]


# root mean squared error or rmse
def measure_rmse(actual, predicted):
    return sqrt(mean_squared_error(actual, predicted))


# split a univariate dataset into train/test sets
def train_test_split(data, n_test):
    return data[:-n_test], data[-n_test:]


# walk-forward validation for univariate data
def walk_forward_validation(data, n_test, cfg):
    predictions = list()
    # split dataset
    train, test = train_test_split(data, n_test)
    # seed history with training dataset
    history = [x for x in train]
    # step over each time-step in the test set
    for i in range(len(test)):
        # fit model and make forecast for history
        yhat = sarima_forecast(history, cfg)
        # store forecast in list of predictions
        predictions.append(yhat)
        # add actual observation to history for the next loop
        history.append(test[i])
    # estimate prediction error
    error = measure_rmse(test, predictions)
    return error


# score a model, return None on failure
def score_model(data, n_test, cfg, debug=False):
    result = None
    # convert config to a key
    key = str(cfg)
    # show all warnings and fail on exception if debugging
    if debug:
        result = walk_forward_validation(data, n_test, cfg)
    else:
        # one failure during model validation suggests an unstable config
        try:
            # never show warnings when grid searching, too noisy
            with catch_warnings():
                filterwarnings("ignore")
                result = walk_forward_validation(data, n_test, cfg)
        except:
            error = None
    # check for an interesting result
    if result is not None:
        print(' > Model[%s] %.3f' % (key, result))
    return (key, result)


# grid search configs
def grid_search(data, cfg_list, n_test, parallel=True):
    scores = None
    if parallel:
        # execute configs in parallel
        executor = Parallel(n_jobs=cpu_count(), backend='multiprocessing')
        tasks = (delayed(score_model)(data, n_test, cfg) for cfg in cfg_list)
        scores = executor(tasks)
    else:
        scores = [score_model(data, n_test, cfg) for cfg in cfg_list]
    # remove empty results
    scores = [r for r in scores if r[1] != None]
    # sort configs by error, asc
    scores.sort(key=lambda tup: tup[1])
    return scores


# create a set of sarima configs to try
def sarima_configs(seasonal=[144]):
    models = list()
    # define config lists
    p_params = [0, 1, 2]
    d_params = [0, 1]
    q_params = [0, 1, 2]
    t_params = ['n', 'c', 't', 'ct']
    P_params = [0, 1, 2]
    D_params = [0, 1]
    Q_params = [0, 1, 2]
    m_params = seasonal
    # create config instances
    for p in p_params:
        for d in d_params:
            for q in q_params:
                for t in t_params:
                    for P in P_params:
                        for D in D_params:
                            for Q in Q_params:
                                for m in m_params:
                                    cfg = [(p, d, q), (P, D, Q, m), t]
                                    models.append(cfg)
    return models

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

def movingaverage(values, window_size):
    weights = (np.ones(window_size))/window_size
    a=np.ones(1)
    return lfilter(weights,a,values)

csv_reader = pd.read_csv('/home/wxiong/seer_remote/EEG_timewindowarr_SA0124_15s.csv',sep=',',header=None)
t_window_arr= csv_reader.values
csv_reader = pd.read_csv('/home/wxiong/seer_remote/EEGvariance_SA0124_15s_3h.csv',sep=',',header=None)
Raw_variance_EEG= csv_reader.values
csv_reader = pd.read_csv('/home/wxiong/seer_remote/EEGauto_SA0124_15s_3h.csv',sep=',',header=None)
Raw_auto_EEG= csv_reader.values
Raw_variance_EEG_arr=[]
for item in Raw_variance_EEG:
    Raw_variance_EEG_arr.append(float(item))
Raw_auto_EEG_arr=[]
for item in Raw_auto_EEG:
    Raw_auto_EEG_arr.append(float(item))
var_arr=[]
for item in Raw_variance_EEG_arr:
    if item<1e-8:
        var_arr.append(item)
    else:
        var_arr.append(var_arr[-1])
Raw_variance_EEG=var_arr
Raw_variance_EEG=Raw_variance_EEG[0:19624]
medium_rhythm_var_arr_3=movingaverage(Raw_variance_EEG,240*6)
long_rhythm_var_arr=medium_rhythm_var_arr_3[240*6:]
diff_EEGvar = np.diff(long_rhythm_var_arr)


value_arr=[]
for item in Raw_auto_EEG_arr:
    if item<500:
        value_arr.append(item)
    else:
        value_arr.append(value_arr[-1])
Raw_auto_EEG_arr=value_arr
Raw_auto_EEG=Raw_auto_EEG_arr[0:19624]
medium_rhythm_value_arr_3=movingaverage(Raw_auto_EEG,240*6)
long_rhythm_value_arr=medium_rhythm_value_arr_3[240*6:]
diff_EEGauto = np.diff(long_rhythm_value_arr)


target_arr = []
index=[]
for i in range(454):
    target_arr.append(long_rhythm_value_arr[i * 40])
    index.append(i * 40)

if __name__ == '__main__':
    # define dataset
    data = target_arr
    # print(data)
    # data split
    n_test = 154
    # model configs
    cfg_list = sarima_configs()
    # grid search
    scores = grid_search(data, cfg_list, n_test)
    print('done')
    # list top 3 configs
    for cfg, error in scores[:3]:
        print(cfg, error)






