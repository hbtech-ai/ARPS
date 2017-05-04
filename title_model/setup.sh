#!/usr/bin/env bash

# create and own the directories to store results locally
save_dir='/var/lib/data_set'
model_dir='/var/lib/data_set/model'
log_dir='/var/lib/data_set/log'

sudo mkdir -p $model_dir
sudo mkdir -p $log_dir
sudo chown -R "$USER" $save_dir

cd data && sudo cp 'train_data.txt' 'dev_data.txt' $save_dir
