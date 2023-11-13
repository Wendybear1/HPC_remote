from __future__ import division
from numpy import array
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import numpy as np
from scipy.signal import butter, lfilter,iirfilter
import pandas as pd
from math import sqrt
from numpy import split
from sklearn.metrics import mean_squared_error

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




### multiple step forcasting


# split a univariate dataset into train/test sets
def split_dataset(data):
    # split into standard weeks
    train, test = data[1:-(240*24-1)], data[-(240*24-1):-23]
    # restructure into windows of weekly data
    train = array(split(train, len(train) / 24))
    test = array(split(test, len(test) / 24))
    return train, test


# evaluate one or more weekly forecasts against expected values
def evaluate_forecasts(actual, predicted):
    scores = list()
    # calculate an RMSE score for each day
    for i in range(actual.shape[1]):
        # calculate mse
        mse = mean_squared_error(actual[:, i], predicted[:, i])
        # calculate rmse
        rmse = sqrt(mse)
        # store
        scores.append(rmse)
    # calculate overall RMSE
    s = 0
    for row in range(actual.shape[0]):
        for col in range(actual.shape[1]):
            s += (actual[row, col] - predicted[row, col]) ** 2
    score = sqrt(s / (actual.shape[0] * actual.shape[1]))
    return score, scores


# summarize scores
def summarize_scores(name, score, scores):
    s_scores = ', '.join(['%.1f' % s for s in scores])
    print('%s: [%.3f] %s' % (name, score, s_scores))


# convert history into inputs and outputs
def to_supervised(train, n_input, n_out=24):
    # flatten data
    data = train.reshape((train.shape[0] * train.shape[1], train.shape[2]))
    X, y = list(), list()
    in_start = 0
    # step over the entire history one time step at a time
    for _ in range(len(data)):
        # define the end of the input sequence
        in_end = in_start + n_input
        out_end = in_end + n_out
        # ensure we have enough data for this instance
        if out_end <= len(data):
            x_input = data[in_start:in_end, 0]
            x_input = x_input.reshape((len(x_input), 1))
            X.append(x_input)
            y.append(data[in_end:out_end, 0])
        # move along one time step
        in_start += 1
    return array(X), array(y)


# train the model
def build_model(train, n_input):
    # prepare data
    train_x, train_y = to_supervised(train, n_input)
    # define parameters
    verbose, epochs, batch_size = 0, 70, 16
    n_timesteps, n_features, n_outputs = train_x.shape[1], train_x.shape[2], train_y.shape[1]
    # define model
    model = Sequential()
    # model.add(LSTM(200, activation='relu', input_shape=(n_timesteps, n_features)))
    # model.add(Dense(100, activation='relu'))
    model.add(LSTM(4, activation='relu', input_shape=(n_timesteps, n_features)))
    model.add(Dense(1, activation='relu'))
    model.add(Dense(n_outputs))
    model.compile(loss='mse', optimizer='adam')
    # fit network
    model.fit(train_x, train_y, epochs=epochs, batch_size=batch_size, verbose=verbose)
    return model


# make a forecast
def forecast(model, history, n_input):
    # flatten data
    data = array(history)
    data = data.reshape((data.shape[0] * data.shape[1], data.shape[2]))
    # retrieve last observations for input data
    input_x = data[-n_input:, 0]
    # reshape into [1, n_input, 1]
    input_x = input_x.reshape((1, len(input_x), 1))
    # forecast the next week
    yhat = model.predict(input_x, verbose=0)
    # we only want the vector forecast
    yhat = yhat[0]
    return yhat


# evaluate a single model
def evaluate_model(train, test, n_input):
    # fit model
    model = build_model(train, n_input)
    # history is a list of weekly data
    history = [x for x in train]
    # walk-forward validation over each week
    predictions = list()
    for i in range(len(test)):
        # predict the week
        yhat_sequence = forecast(model, history, n_input)
        # store the predictions
        predictions.append(yhat_sequence)
        # get real observation and add to history for predicting the next week
        history.append(test[i, :])
    # evaluate predictions days for each week
    predictions = array(predictions)
    print(predictions)
    np.savetxt("LSTM_forecast_Cz_3hcycle_EEGvar_SA0124.csv", predictions, delimiter=",", fmt='%s')
    score, scores = evaluate_forecasts(test[:, :, 0], predictions)
    return score, scores


csv_reader = pd.read_csv('/fred/oz132/EEGresult/channels/Cz_EEGvariance_SA0124_15s_3h.csv',sep=',',header=None)
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


medium_rhythm_var_arr_1=movingaverage(Raw_var_EEG_arr,240*6)
# data={'EEGvariance': list(medium_rhythm_var_arr_1[0:240*24*6])}
data={'EEGvariance': list(medium_rhythm_var_arr_1[0:240*24*3])}
df = pd.DataFrame(data)
dataset = df.values

# split into train and test
train, test = split_dataset(dataset)
# evaluate model and get scores
n_input = 240
score, scores = evaluate_model(train, test, n_input)
# summarize scores
summarize_scores('lstm', score, scores)
print(scores)

# # plot scores
# days = ['sun', 'mon', 'tue', 'wed', 'thr', 'fri', 'sat']
# pyplot.plot(days, scores, marker='o', label='lstm')
# pyplot.show()
np.savetxt("LSTM_forecast_Cz_3hcycle_EEGvar_SA0124.csv", scores, delimiter=",", fmt='%s')