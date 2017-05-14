#!/usr/bin/env python3
import random 

file_origin = open('train_pos.txt', 'r')
lines = file_origin.readlines()
file_origin.close()

file_origin = open('train_neg.txt', 'r')
lines += file_origin.readlines()
file_origin.close()

random.shuffle(lines)

train_str = ''
test_str = ''
trans_str = ''

test_idx = random.sample(range(len(lines)), int(len(lines)*0.2))

for i, l in enumerate(lines):
	line_list = l.strip().split('\t')
	if line_list[1] == '0':
		line_list[1] = '-1'
	trans_str = line_list[1] + '\t' + line_list[0] + '\n'
	if i in test_idx:
		test_str += trans_str
	else:
		train_str += trans_str

file_trans = open('data_seged.train', 'w')
file_trans.writelines(train_str)
file_trans.close()

file_trans = open('data_seged.test', 'w')
file_trans.writelines(test_str)
file_trans.close()


