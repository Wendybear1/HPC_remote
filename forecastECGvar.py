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


# from numpy import array
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




from statsmodels.tsa.api import SARIMAX
# csv_reader = pd.read_csv('/fred/oz132/seer_remote/ecg_data_result_PNES/RRI_ch31_rawvariance_QLD1230_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(26):
#     var_arr=Raw_var_EEG_arr[0:(18720+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(18720+240*3*k)]
#     # var_trans=hilbert(long_var_plot)
#     # var_phase = np.angle(var_trans)
#
#     phase_short_EEGvar_arr=long_var_plot
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#     target_arr = []
#     for i in range(432):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 0, 1)
#     my_seasonal_order = (1, 0, 1, 72)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(432, 449))
# np.savetxt("cycles6hd0m72_ch31_forecast81hsignal_3hcycle_RRIvar_QLD1230.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


# from statsmodels.tsa.api import SARIMAX
# ###forecast EEG var
# csv_reader = pd.read_csv('/home/wxiong/seer_remote/ecg_data_result_PNES/RRI_ch31_rawvariance_VIC2835_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(11):
#     var_arr=Raw_var_EEG_arr[0:(7940+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,20*1)
#
#     long_var_plot = long_rhythm_var_arr[(20*1+240*3*k):(7940+240*3*k)]
#     phase_short_EEGvar_arr=long_var_plot
#
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#
#     target_arr = []
#     for i in range(198):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 1, 1)
#     my_seasonal_order = (1, 1, 1, 144)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(198, 215))
# np.savetxt("cycles5min_ch31_forecast33hsignal_3hcycle_RRIvar_VIC2835.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')




# csv_reader = pd.read_csv('/fred/oz132/seer_remote/ecg_data_result_PNES/RRI_ch31_rawvariance_SA1243_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(27):
#     var_arr=Raw_var_EEG_arr[0:(19450+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(19450+240*3*k)]
#     # var_trans=hilbert(long_var_plot)
#     # var_phase = np.angle(var_trans)
#
#     phase_short_EEGvar_arr=long_var_plot
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#     target_arr = []
#     for i in range(450):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 1, 1)
#     my_seasonal_order = (1, 1, 1, 72)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(450, 467))
# np.savetxt("cycles6hm72_ch31_forecast81hsignal_3hcycle_RRIvar_SA1243_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


csv_reader = pd.read_csv('/fred/oz132/seer_remote/ecg_data_result_PNES/RRI_ch31_rawvariance_QLD1282_15s_3h.csv',sep=',',header=None)
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
    # var_trans=hilbert(long_var_plot)
    # var_phase = np.angle(var_trans)

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
np.savetxt("cycles6hm72_ch31_forecast81hsignal_3hcycle_RRIvar_QLD1282_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


# def split_sequence(sequence, n_steps_in, n_steps_out):
#     X, y = list(), list()
#     for i in range(len(sequence)):
#     # find the end of this pattern
#         end_ix = i + n_steps_in
#         out_end_ix = end_ix + n_steps_out
#     # check if we are beyond the sequence
#         if out_end_ix > len(sequence):
#             break
#     # gather input and output parts of the pattern
#         seq_x, seq_y = sequence[i:end_ix], sequence[end_ix:out_end_ix]
#         X.append(seq_x)
#         y.append(seq_y)
#     return array(X), array(y)
#
#
# fore_arr_EEGvars=[]
# for k in range(27):
# # for k in range(1):
#     var_arr=Raw_var_EEG_arr[0:(19450+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(19450+240*3*k)]
#     rolmean_short_EEGvar=long_var_plot
#
#
#     target_arr = []
#     for i in range(450):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
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
# np.savetxt("activation_LSTM_ch31_RRIvar_QLD0290.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')



# from statsmodels.tsa.api import SARIMAX
#
# csv_reader = pd.read_csv('/fred/oz132/ECGresult/PNES/RRI_ch31_rawvariance_QLD2307_15s_3h.csv',sep=',',header=None)
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
#     # var_trans=hilbert(long_var_plot)
#     # var_phase = np.angle(var_trans)
#
#     phase_short_EEGvar_arr=long_var_plot
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#     target_arr = []
#     for i in range(342):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 0, 1)
#     my_seasonal_order = (1, 0, 1, 216)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(342, 359))
# np.savetxt("cycles24hd0m216_ch31_forecast81hsignal_3hcycle_RRIvar_QLD2307_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')



# from statsmodels.tsa.api import SARIMAX
#
# csv_reader = pd.read_csv('/fred/oz132/ECGresult/PNES/RRI_ch31_rawvariance_QLD3694_15s_3h.csv',sep=',',header=None)
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
#     my_seasonal_order = (1, 1, 1, 144)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(288, 305))
# np.savetxt("cycles6h_ch31_forecast63hsignal_3hcycle_RRIvar_QLD3694_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')



# from statsmodels.tsa.api import SARIMAX
#
# csv_reader = pd.read_csv('/fred/oz132/ECGresult/PNES/RRI_ch31_rawvariance_NSW1402_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(21):
#     var_arr=Raw_var_EEG_arr[0:(15120+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*12)
#     long_var_plot = long_rhythm_var_arr[(240*12+240*3*k):(15120+240*3*k)]
#     # var_trans=hilbert(long_var_plot)
#     # var_phase = np.angle(var_trans)
#
#     phase_short_EEGvar_arr=long_var_plot
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#     target_arr = []
#     for i in range(306):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 1, 1)
#     my_seasonal_order = (1, 1, 1, 72)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(306, 323))
# np.savetxt("cycles12hm72_ch31_forecast63hsignal_3hcycle_RRIvar_NSW1402_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')





# from statsmodels.tsa.api import SARIMAX
# csv_reader = pd.read_csv('/fred/oz132/seer_remote/ecg_data_result_PNES/RRI_ch31_rawvariance_SA1243_15s_3h.csv',sep=',',header=None)
# Raw_variance_EEG= csv_reader.values
# Raw_var_EEG_arr=[]
# for item in Raw_variance_EEG:
#     Raw_var_EEG_arr.append(float(item))
#
# fore_arr_EEGvars=[]
# save_data_EEGvars=[]
# for k in range(27):
#     var_arr=Raw_var_EEG_arr[0:(19450+240*3*k)]
#     long_rhythm_var_arr=movingaverage(var_arr,240*6)
#     long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(19450+240*3*k)]
#     # var_trans=hilbert(long_var_plot)
#     # var_phase = np.angle(var_trans)
#
#     phase_short_EEGvar_arr=long_var_plot
#     rolmean_short_EEGvar=phase_short_EEGvar_arr
#
#     target_arr = []
#     for i in range(450):
#         target_arr.append(rolmean_short_EEGvar[i * 40])
#     data = target_arr
#     my_order = (1, 0, 1)
#     my_seasonal_order = (1, 0, 1, 216)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(450, 467))
# np.savetxt("cycles6hd0m216_ch31_forecast81hsignal_3hcycle_RRIvar_SA1243_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')


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
#     my_order = (1, 0, 1)
#     my_seasonal_order = (1, 0, 1, 288)
#     model = SARIMAX(data, order=my_order, seasonal_order=my_seasonal_order)
#     model_fit = model.fit()
#     fore_arr_EEGvars.append(model_fit.predict(396, 413))
# np.savetxt("cycles12hd0m288_ch31_forecast78hsignal_3hcycle_RRIvar_WA0305_2022.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')



