# -*- coding:utf-8 -*-
from keras.layers.convolutional import MaxPooling1D, Conv1D
from keras.layers.core import Flatten, Dropout, Dense
from keras.layers.normalization import BatchNormalization
from keras.layers import Merge
from keras.layers.recurrent import GRU
from keras.models import Sequential

from model.config import SAMPLE_LENGTH


def get_nn_model(nn_model, embedding, output_length):
    if nn_model == 'cnn':
        return cnn(embedding_size=embedding, output_length=output_length)
    elif nn_model == 'rnn':
        return rnn(embedding_size=embedding, output_length=output_length)
    else:
        raise ValueError("Unknown NN type: {}".format(nn_model))


def cnn(embedding_size, output_length):
    """ Create and return a keras model of a CNN """
    NB_FILTER = 256
    NGRAM_LENGTHS = [1, 2, 3, 4, 5]

    conv_layers = []
    for ngram_length in NGRAM_LENGTHS:
        ngram_layer = Sequential()
        ngram_layer.add(Conv1D(
            NB_FILTER,
            ngram_length,
            kernel_initializer='lecun_uniform',
            activation='tanh',
            input_shape=(SAMPLE_LENGTH, embedding_size)
        ))
        pool_length = SAMPLE_LENGTH - ngram_length + 1
        ngram_layer.add(MaxPooling1D(pool_size=pool_length))
        conv_layers.append(ngram_layer)

    model = Sequential()
    model.add(Merge(conv_layers, mode='concat'))

    model.add(Dropout(0.5))
    model.add(Flatten())

    model.add(Dense(output_length, activation='sigmoid'))

    model.compile(
        loss='binary_crossentropy',
        optimizer='adam',
        metrics=['accuracy'],
    )

    return model


def rnn(embedding_size, output_length):
    """ Create and return a keras model of a RNN """
    HIDDEN_LAYER_SIZE = 256

    model = Sequential()

    model.add(GRU(
        HIDDEN_LAYER_SIZE,
        input_dim=embedding_size,
        input_length=SAMPLE_LENGTH,
        init='glorot_uniform',
        inner_init='normal',
        activation='relu',
    ))
    model.add(BatchNormalization())
    model.add(Dropout(0.1))

    model.add(Dense(output_length, activation='sigmoid'))

    model.compile(
        loss='binary_crossentropy',
        optimizer='adam',
        metrics=['accuracy'],
    )

    return model
