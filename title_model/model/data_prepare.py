# -*- coding:utf-8 -*-
from __future__ import print_function

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import random
import numpy as np
from config import FLAGS

PAD_ID = FLAGS.PAD_ID
def zero_pad(X, seq_len):
    return np.array([x[:seq_len - 1] + [PAD_ID] * max(seq_len - len(x), 1) for x in X])

def get_batch(data):
    batch_data = []
    for i in range(FLAGS.batch_size):
        batch_data.append(random.choice(data))
    data = [x[0].split('\t')[0].split(' ') for x in batch_data]
    label = [int(x[0].split('\t')[1][0]) for x in batch_data]
    length = [len(x) for x in data]
    return [[int(x) for x in y] for y in zero_pad(data, FLAGS.max_seq_length)], label, length

def get_train_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        size = len(lines)
        index = np.arange(size)
        np.random.shuffle(index)
        # print(max(map(lambda x: len(x), [y for y in map(lambda y: y.split(' '), lines)])))
        data = [[lines[x]] for x in index]
    return data
