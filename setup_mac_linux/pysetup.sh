#!/bin/sh
now=$1
address=$2
temp_path=$3

cd $temp_path
wget https://www.python.org/ftp/python/3.9.5/Python-3.9.5.tgz
yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel
tar zxvf Python-3.9.5.tgz
cd Python-3.9.5
./configure --prefix="$address/Python-3.9.5/"
make && make install