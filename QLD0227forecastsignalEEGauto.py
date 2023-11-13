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
# from statsmodels.tsa.api import SARIMAX
from numpy import array
# from keras.models import Sequential
# from keras.layers import LSTM
# from keras.layers import Dense
from scipy.signal import butter, lfilter,iirfilter


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


def split_sequence(sequence, n_steps_in, n_steps_out):
    X, y = list(), list()
    for i in range(len(sequence)):
    # find the end of this pattern
        end_ix = i + n_steps_in
        out_end_ix = end_ix + n_steps_out
    # check if we are beyond the sequence
        if out_end_ix > len(sequence):
            break
    # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix:out_end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)



# from statsmodels.tsa.api import SARIMAX

# csv_reader = pd.read_csv('/home/wxiong/seer_remote/eeg_data_result_PNES/Cz_EEGauto_ACT0128_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
#
# value_arr=[0]
# for item in Raw_var_EEG_arr:
#     if item<500:
#         value_arr.append(item)
#     else:
#         value_arr.append(value_arr[-1])
# Raw_var_EEG_arr=value_arr
#
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(24):
#     var_arr=Raw_var_EEG_arr[0:(17280+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(17280+240*3*k)]
#     rolmean_short_EEGvar=long_var_plot
#
#
#     target_arr = []
#     for i in range(396):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
# #     data = target_arr
# #     my_order = (1, 1, 1)
# #     my_seasonal_order = (1, 1, 1, 144)
# #     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
# #     model_fit = model.fit()
# #     fore_arr_EEGvars.append(model_fit.predict(288, 305))
# # np.savetxt("cycles24h_Cz_forecast72hsignal_3hcycle_EEGauto_ACT0128.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')
#
#     raw_seq = target_arr
#     n_steps_in, n_steps_out = 24*6, 3*6
#     X, y = split_sequence(raw_seq, n_steps_in, n_steps_out)
#
#     n_features = 1
#     X = X.reshape((X.shape[0], X.shape[1], n_features))
#
#     model = Sequential()
#     # model.add(LSTM(50, activation="relu", return_sequences=True, input_shape=(n_steps_in, n_features)))
#     # model.add(LSTM(50, activation="relu" ))
#
#     model.add(LSTM(50, activation="tanh", recurrent_activation="sigmoid", return_sequences=True,
#                input_shape=(n_steps_in, n_features)))
#     model.add(LSTM(50, activation="tanh", recurrent_activation="sigmoid", ))
#     model.add(Dense(n_steps_out))
#     model.compile(optimizer='adam', loss='mse')
#     model.fit(X, y, epochs=200, verbose=0)
#
#     x_input = array(rolmean_short_EEGvar[-24*6:])
#     x_input = x_input.reshape((1, n_steps_in, n_features))
#     yhat = model.predict(x_input, verbose=0)
#     fore_arr_EEGvars.append(yhat[0])
# np.savetxt("activation_LSTM_Cz_EEGauto_ACT0128.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


# csv_reader = pd.read_csv('/home/wxiong/seer_remote/eeg_data_result_PNES/Cz_EEGauto_QLD1230_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
# # var_arr=[]
# # for item in Raw_var_EEG_arr:
# #     if item<1e-8:
# #         var_arr.append(item)
# #     else:
# #         var_arr.append(var_arr[-1])
# # Raw_var_EEG_arr=var_arr
#
# var_arr=[]
# for item in Raw_var_EEG_arr:
#     if item<500:
#         var_arr.append(item)
#     else:
#         var_arr.append(var_arr[-1])
# Raw_var_EEG_arr=var_arr
#
#
#
# fore_arr_EEGvars=[]
# for k in range(26):
# # for k in range(2):
#     var_arr=Raw_var_EEG_arr[0:(18720+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(18720+240*3*k)]
#     # long_var_plot = long_rhythm_var_arr[(240 * 0 + 240 * 3 * k):(18720 + 240 * 3 * k)]
#     var_trans = hilbert(long_var_plot)
#     value_phase = np.angle(var_trans)
#     rolmean_short_EEGvar=value_phase
#
#     target_arr = []
#     for i in range(432):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#
#     raw_seq = target_arr
#     n_steps_in, n_steps_out = 24*6, 3*6
#     X, y = split_sequence(raw_seq, n_steps_in, n_steps_out)
#
#     n_features = 1
#     X = X.reshape((X.shape[0], X.shape[1], n_features))
#     model = Sequential()
#     # model.add(LSTM(50, activation='relu', input_shape=(n_steps_in, n_features)))
#     # model.add(LSTM(50, activation="relu", return_sequences=True, input_shape=(n_steps_in, n_features)))
#     # model.add(LSTM(50, activation="relu" ))
#
#     model.add(LSTM(50, activation="tanh",recurrent_activation="sigmoid", return_sequences=True,input_shape=(n_steps_in, n_features)))
#     model.add(LSTM(50, activation="tanh",recurrent_activation="sigmoid",))
#     model.add(Dense(n_steps_out))
#     model.compile(optimizer='adam', loss='mse')
#     model.fit(X, y, epochs=200, verbose=0)
#
#     x_input = array(rolmean_short_EEGvar[-24*6:])
#     x_input = x_input.reshape((1, n_steps_in, n_features))
#     yhat = model.predict(x_input, verbose=0)
#     fore_arr_EEGvars.append(yhat[0])
#     print(yhat)
# np.savetxt("phases_LSTM_Ch31_EEGauto_QLD1230.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')



from statsmodels.tsa.api import SARIMAX


# csv_reader = pd.read_csv('/home/wxiong/seer_remote/eeg_data_result_PNES/Cz_EEGauto_VIC2835_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
#
# value_arr=[0]
# for item in Raw_var_EEG_arr:
#     if item<500:
#         value_arr.append(item)
#     else:
#         value_arr.append(value_arr[-1])
# Raw_var_EEG_arr=value_arr
#
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(11):
#     var_arr=Raw_var_EEG_arr[0:(7940+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(7940+240*3*k)]
#
#     phase_short_EEGvar_arr=long_var_plot
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#
#     target_arr = []
#     for i in range(162):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 1, 1)
#     my_seasonal_order = (1, 1, 1, 144)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     # print(model_fit.summary())
#     fore_arr_EEGvars.append(model_fit.predict(162, 179))
#
# np.savetxt("cycles6h_Cz_forecast33hsignal_3hcycle_EEGauto_VIC2835.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


csv_reader = pd.read_csv('/fred/oz132/channels/PNES/channels/VIC0829_pure/Cz_EEGauto_VIC0829_15s_3h.csv',sep=',',header=None)
Raw_variance_EEG= csv_reader.values
Raw_var_EEG_arr=[]
for item in Raw_variance_EEG:
    Raw_var_EEG_arr.append(float(item))


value_arr=[0]
for item in Raw_var_EEG_arr:
    if item<500:
        value_arr.append(item)
    else:
        value_arr.append(value_arr[-1])
Raw_var_EEG_arr=value_arr


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
    my_seasonal_order = (1, 0, 1, 144)
    model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
    model_fit = model.fit()
    print(model_fit.summary())
    fore_arr_EEGvars.append(model_fit.predict(450, 467))

np.savetxt("cycles6hd0_Cz_forecast81hsignal_3hcycle_EEGauto_VIC0829.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


# csv_reader = pd.read_csv('/fred/oz132/channels/PNES/channels/QLD0290_pure/Cz_EEGauto_QLD0290_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
#
# value_arr=[0]
# for item in Raw_var_EEG_arr:
#     if item<500:
#         value_arr.append(item)
#     else:
#         value_arr.append(value_arr[-1])
# Raw_var_EEG_arr=value_arr
#
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(27):
#     var_arr=Raw_var_EEG_arr[0:(19450+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(19450+240*3*k)]
#
#     phase_short_EEGvar_arr=long_var_plot
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#
#     target_arr = []
#     for i in range(450):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 0, 1)
#     my_seasonal_order = (1, 0, 1, 144)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     print(model_fit.summary())
#     fore_arr_EEGvars.append(model_fit.predict(450, 467))
#
# np.savetxt("cycles6hd0_Cz_forecast81hsignal_3hcycle_EEGauto_QLD0290_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


# csv_reader = pd.read_csv('/fred/oz132/channels/PNES/channels/QLD3694_pure/Cz_EEGauto_QLD3694_15s_3h.csv',sep=',',header=None)
# # Raw_variance_EEG= csv_reader.values
# # Raw_var_EEG_arr=[]
# # for item in Raw_variance_EEG:
# #     Raw_var_EEG_arr.append(float(item))
# #
# #
# # value_arr=[0]
# # for item in Raw_var_EEG_arr:
# #     if item<500:
# #         value_arr.append(item)
# #     else:
# #         value_arr.append(value_arr[-1])
# # Raw_var_EEG_arr=value_arr
# #
# #
# # fore_arr_EEGvars=[]
# # save_data_EEGvars=[]
# # for k in range(20):
# #     var_arr=Raw_var_EEG_arr[0:(14400+240*3*k)]
# #     long_rhythm_var_arr=movingaverage(var_arr,240*12)
# #     long_var_plot = long_rhythm_var_arr[(240*12+240*3*k):(14400+240*3*k)]
# #
# #     phase_short_EEGvar_arr=long_var_plot
# #     rolmean_short_EEGvar=phase_short_EEGvar_arr
# #
# #
# #     target_arr = []
# #     for i in range(288):
# #         target_arr.append(rolmean_short_EEGvar[i * 40])
# #     data = target_arr
# #     my_order = (1, 1, 1)
# #     my_seasonal_order = (1, 1, 1, 144)
# #     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
# #     model_fit = model.fit()
# #     print(model_fit.summary())
# #     fore_arr_EEGvars.append(model_fit.predict(288, 305))
# #
# # np.savetxt("cycles12h_Cz_forecast60hsignal_3hcycle_EEGauto_QLD3694_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')



# csv_reader = pd.read_csv('/fred/oz132/channels/PNES/channels/ACT0128_pure/Cz_EEGauto_ACT0128_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
#
# value_arr=[0]
# for item in Raw_var_EEG_arr:
#     if item<500:
#         value_arr.append(item)
#     else:
#         value_arr.append(value_arr[-1])
# Raw_var_EEG_arr=value_arr
#
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(24):
#     var_arr=Raw_var_EEG_arr[0:(17280+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(17280+240*3*k)]
#
#     phase_short_EEGvar_arr=long_var_plot
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#
#     target_arr = []
#     for i in range(396):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 0, 1)
#     my_seasonal_order = (1, 0, 1, 144)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     print(model_fit.summary())
#     fore_arr_EEGvars.append(model_fit.predict(396, 413))
#
# np.savetxt("cycles6hd0_Cz_forecast72hsignal_3hcycle_EEGauto_ACT0128_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')




# csv_reader = pd.read_csv('/fred/oz132/channels/PNES/channels/QLD2982_pure/Cz_EEGauto_QLD2982_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
#
# value_arr=[0]
# for item in Raw_var_EEG_arr:
#     if item<500:
#         value_arr.append(item)
#     else:
#         value_arr.append(value_arr[-1])
# Raw_var_EEG_arr=value_arr
#
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(26):
#     var_arr=Raw_var_EEG_arr[0:(18720+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(18720+240*3*k)]
#
#     phase_short_EEGvar_arr=long_var_plot
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#     target_arr = []
#     for i in range(432):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 1, 1)
#     my_seasonal_order = (1, 1, 1, 216)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     # print(model_fit.summary())
#     fore_arr_EEGvars.append(model_fit.predict(432, 449))
#
# np.savetxt("cycles6hm216_Cz_forecast78hsignal_3hcycle_EEGauto_QLD2982_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')








