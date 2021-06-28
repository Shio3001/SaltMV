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

#/Users/maruyama/opt/anaconda3/lib/python3.8/config-3.8-darwin
#(base) 20N1101361maruyamatakuma:NankokuMovieMaker maruyama$ LIBRARY_PATH=/usr/local/Cellar/boost-python3/1.76.0/lib