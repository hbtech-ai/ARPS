#!/usr/bin/env bash

# create and own the directories to store results locally
save_dir='/var/lib/spider_save'

sudo mkdir -p $save_dir
sudo chown -R "$USER" $save_dir
