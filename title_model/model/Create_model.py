# -*- coding:utf-8 -*-
from __future__ import print_function

import tensorflow as tf
from config import FLAGS
from classification_title import Title_Network

def create_model(sess, batch_size, forward_only):
	model = Title_Network(batch_size, forward_only)

	ckpt = tf.train.get_checkpoint_state(FLAGS.model_path)
	if ckpt:
		print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
		model.saver.restore(sess, ckpt.model_checkpoint_path)
	else:
		print("Created model with fresh parameters.")
		sess.run(tf.global_variables_initializer())
	return model

