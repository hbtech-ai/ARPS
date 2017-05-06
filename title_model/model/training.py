# -*- coding:utf-8 -*-
from __future__ import print_function

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import tensorflow as tf
from config import FLAGS
from Create_model import create_model
from data_prepare import get_train_data, get_batch

def train():
	# prepare data
	train_data = get_train_data(FLAGS.train_path)
	dev_data = get_train_data(FLAGS.dev_path)

	# loss and accuracy
	cur_step, losses, accuracy = 0, 0.0, 0.0

	# training
	with tf.Session() as sess:
		model = create_model(sess, FLAGS.batch_size, forward_only=False)
		summary_writer = tf.summary.FileWriter(FLAGS.log_path + '/dev', sess.graph)
		print('Start training:')
		while True:
			# get data, label and sequence length
			batch_data, batch_label, seq_length = get_batch(train_data)

			# start training
			loss, acc, _ = model.running_step(sess, batch_data, seq_length, batch_label)
			losses += loss / FLAGS.check_point
			accuracy += acc / FLAGS.check_point
			cur_step += 1

			if cur_step % FLAGS.check_point == 0:
				print('Step {}:\tloss: {:.3f} acc: {:.3f}'.format(model.global_step.eval(), losses, accuracy))

				# test
				batch_dev, dev_label, dev_length = get_batch(dev_data)
				dev_loss, dev_acc, d_val = model.running_step(sess, batch_dev, dev_length, dev_label, mode="dev")
				print(' ' * 8 + '\tloss: {:.3f} acc: {:.3f}'.format(dev_loss, dev_acc))

				# save model
				checkpoint_path = os.path.join(FLAGS.model_path + '/', 'model.ckpt')
				model.saver.save(sess, checkpoint_path, global_step=model.global_step)

				# visualization
				global_step = sess.run(model.global_step)
				summary_writer.add_summary(d_val, global_step=global_step)

				step, losses, accuracy = 0, 0.0, 0.0

if __name__ == '__main__':
	train()
