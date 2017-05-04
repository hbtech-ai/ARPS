# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import tensorflow as tf
from config import FLAGS
from tensorflow.contrib.rnn import GRUCell
from tensorflow.python.ops.rnn import bidirectional_dynamic_rnn as bi_rnn

class Title_Network(object):
	def __init__(self, batch_size, forward_only=False):
		self.batch_size = batch_size
		self.learning_rate = FLAGS.learning_rate
		self.max_seq_length = FLAGS.max_seq_length
		self.embedding_size = FLAGS.embedding_size
		self.vocab_size = FLAGS.vocab_size
		self.hidden_size = FLAGS.hidden_size
		self.attention_size = FLAGS.attention_size
		self.class_number = FLAGS.class_number
		self.global_step = tf.Variable(0, trainable=False)

		# input
		self.input = tf.placeholder(tf.int32, [self.batch_size, self.max_seq_length], name="input")
		self.label = tf.placeholder(tf.float32, [self.batch_size], name="label")
		self.seq_length = tf.placeholder(tf.int32, [self.batch_size], name="seq_length")
		self.keep_prob = tf.placeholder(tf.float32)

		# word embedding
		embedding = tf.Variable(tf.random_uniform([self.vocab_size, self.embedding_size], -1.0, 1.0), trainable=True)
		input_embedding = tf.nn.embedding_lookup(embedding, self.input)

		# Bi-GRU
		rnn_outputs, _ = bi_rnn(GRUCell(self.hidden_size), GRUCell(self.hidden_size), inputs=input_embedding, sequence_length=self.seq_length, dtype=tf.float32)

		# attention
		attention_output = self.attention(rnn_outputs)

		# drop
		output = tf.nn.dropout(attention_output, self.keep_prob)

		# softmax, get loss and accuracy
		s_W = tf.Variable(tf.truncated_normal([output.get_shape()[1].value, self.class_number], stddev=0.1))
		s_b = tf.Variable(tf.constant(0., shape=[self.class_number]))
		y = tf.nn.xw_plus_b(output, s_W, s_b, name="y")
		self.y = tf.squeeze(y)

		self.accuracy = 1. - tf.reduce_mean(tf.cast(tf.equal(tf.round(self.y), self.label), tf.float32))
		if not forward_only:
			self.loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=self.y, labels=self.label))

			# optimize
			params = tf.trainable_variables()
			gradidents = tf.gradients(self.loss, params)
			self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
			self.update = self.optimizer.apply_gradients(zip(gradidents, params), global_step=self.global_step)

			# visualization
			self.dev_loss = tf.summary.scalar('dev_loss', self.loss)
			self.dev_acc = tf.summary.scalar('dev_acc', self.accuracy)

		# save model
		self.saver = tf.train.Saver(tf.global_variables())

	def attention(self, inputs):
		# connect
		if isinstance(inputs, tuple):
			inputs = tf.concat(inputs, 2)

		# get shape
		seq_length = inputs.shape[1].value
		hidden_size = inputs.shape[2].value

		# attention model
		a_W = tf.Variable(tf.random_normal([hidden_size, self.attention_size], stddev=0.1), name='a_W')
		a_b = tf.Variable(tf.random_normal([self.attention_size], stddev=0.1), name='a_b')
		context_vec = tf.Variable(tf.random_normal([self.attention_size], stddev=0.1), name='context_vec')

		output = tf.tanh(tf.matmul(tf.reshape(inputs, [-1, hidden_size]), a_W) + tf.reshape(a_b, [1, -1]))
		output = tf.matmul(output, tf.reshape(context_vec, [-1, 1]))
		exp_output = tf.reshape(tf.exp(output), [-1, seq_length])
		alpha = exp_output / tf.reshape(tf.reduce_sum(exp_output, 1), [-1, 1])

		# get attention output
		attention_output = tf.reduce_sum(inputs * tf.reshape(alpha, [-1, seq_length, 1]), 1)

		return attention_output

	def running_step(self, sess, x, seq_length, y, mode="train"):
		# get feed
		input_feed = {self.input.name: x, self.label.name: y, self.seq_length.name: seq_length, self.keep_prob.name: 0.5}

		# run
		if mode == "train":
			output_feed = [self.loss, self.accuracy, self.update]
			output = sess.run(output_feed, feed_dict=input_feed)
		elif mode == "dev":
			output_feed = [self.loss, self.accuracy, tf.summary.merge([self.dev_loss, self.dev_acc])]
			output = sess.run(output_feed, feed_dict=input_feed)
		else:
			output_feed = [self.y, self.accuracy]
			output = sess.run(output_feed, feed_dict=input_feed)

		return output
