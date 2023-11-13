from __future__ import division
from numpy import array
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import numpy as np
from scipy.signal import butter, lfilter,iirfilter
import pandas as pd



# split a univariate sequence into samples
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

def movingaverage(values, window_size):
    weights = (np.ones(window_size))/window_size
    a=np.ones(1)
    return lfilter(weights,a,values)

csv_reader = pd.read_csv('/home/wxiong/seer_remote/eeg_data_result_PNES/Cz_EEGauto_QLD1230_15s_3h.csv',sep=',',header=None)
Raw_variance_EEG= csv_reader.values
Raw_var_EEG_arr=[]
for item in Raw_variance_EEG:
    Raw_var_EEG_arr.append(float(item))

var_arr=[]
for item in Raw_var_EEG_arr:
    if item<500:
        var_arr.append(item)
    else:
        var_arr.append(var_arr[-1])
Raw_var_EEG_arr=var_arr




fore_arr_EEGvars=[]
for k in range(26):
# for k in range(1):
    var_arr=Raw_var_EEG_arr[0:(18720+240*3*k)]
    long_rhythm_var_arr=movingaverage(var_arr,240*6)
    long_var_plot = long_rhythm_var_arr[(240*6+240*3*k):(18720+240*3*k)]
    rolmean_short_EEGvar=long_var_plot


    target_arr = []
    for i in range(432):
        target_arr.append(rolmean_short_EEGvar[i * 40])

    raw_seq = target_arr
    n_steps_in, n_steps_out = 24*6, 3*6
    X, y = split_sequence(raw_seq, n_steps_in, n_steps_out)

    n_features = 1
    X = X.reshape((X.shape[0], X.shape[1], n_features))

    model = Sequential()
    # model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(n_steps_in, n_features)))
    # model.add(LSTM(50, activation='relu'))
    model.add(LSTM(50, activation="tanh", recurrent_activation="sigmoid", return_sequences=True,
               input_shape=(n_steps_in, n_features)))
    model.add(LSTM(50, activation="tanh", recurrent_activation="sigmoid", ))

    model.add(Dense(n_steps_out))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=200, verbose=0)

    x_input = array(rolmean_short_EEGvar[-24*6:])
    x_input = x_input.reshape((1, n_steps_in, n_features))
    yhat = model.predict(x_input, verbose=0)
    fore_arr_EEGvars.append(yhat[0])
np.savetxt("activation_LSTM_Cz_EEGauto_QLD1230.csv", fore_arr_EEGvars, delimiter=",", fmt='%s')