#!/bin/bash

sudo yum update -y
sudo yum install tmux -y
sudo yum install git -y

sudo yum install python3 -y
sudo yum install python-pip -y

cd /home/ec2-user

git clone https://github.com/duy07t1k23cht/pdf-split.git

echo "cd pdf-split && pip install -r requirements.txt && sh run.sh" > run.sh