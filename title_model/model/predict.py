# -*- coding:utf-8 -*-
from __future__ import print_function

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import math
import jieba
import numpy as np
import tensorflow as tf
from config import FLAGS
from data_prepare import zero_pad
from Create_model import create_model

def sigmoid(x):
	return (1. / (1. + math.exp(-x)))

def counts(word, vocab):
	for i, line in enumerate(vocab):
		if line.split('\t')[0] == word:
			return i
	return FLAGS.PAD_ID

def get_sentence(raw):
	raw = ' '.join(jieba.cut(raw)).split(' ')
	with open(FLAGS.vocab_path, 'r') as f:
		lines = f.readlines()
		number = [counts(word, lines) for word in raw]
		f.close()
	return number, len(raw)

def predict():
	title = raw_input()
	with tf.Session() as sess:
		model = create_model(sess, 1, forward_only=True)
		sentence, length = get_sentence(title)
		sentence = zero_pad([sentence], FLAGS.max_seq_length)
		length = np.array([length])
		y, acc = model.running_step(sess, sentence, length, [1], mode="test")
		print("The answer for class of this title is {}.".format(int(round(sigmoid(y)))))

if __name__ == '__main__':
	predict()
