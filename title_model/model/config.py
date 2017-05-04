import os
import tensorflow as tf

save_path = '/var/lib/data_set/'

tf.app.flags.DEFINE_string('train_path', os.path.join(save_path, 'train_data.txt'), 'The path that save data for training')
tf.app.flags.DEFINE_string('dev_path', os.path.join(save_path, 'dev_data.txt'), 'The path that save data for testing')
tf.app.flags.DEFINE_string('model_path', os.path.join(save_path, 'model'), 'The path that save model')
tf.app.flags.DEFINE_string('log_path', os.path.join(save_path, 'log'), 'The path that save visualization')
tf.app.flags.DEFINE_string('vocab_path', os.path.join(save_path, 'vocab.txt'), 'The path that save vocabulary')

tf.app.flags.DEFINE_integer('batch_size', 64, 'Batch size')
tf.app.flags.DEFINE_integer('max_seq_length', 45, 'Max length of sentence')
tf.app.flags.DEFINE_integer('embedding_size', 128, 'Size of word embedding')
tf.app.flags.DEFINE_integer('vocab_size', 20000, 'Size of vocabulary')
tf.app.flags.DEFINE_integer('hidden_size', 128, 'Size of hidden units')
tf.app.flags.DEFINE_integer('attention_size', 64, 'Size of attention units')
tf.app.flags.DEFINE_integer('class_number', 1, 'Number of class')
tf.app.flags.DEFINE_integer('check_point', 10, 'Check number')
tf.app.flags.DEFINE_integer('PAD_ID', 17361, 'The number for padding')

tf.app.flags.DEFINE_float('keep_prob', 0.5, 'Possibility of drop')
tf.app.flags.DEFINE_float('learning_rate', 1e-3, 'Learning rate')

FLAGS = tf.app.flags.FLAGS
