#!/bin/sh
wget -h

now_path = pwd

wget https://www.python.org/ftp/python/3.9.5/Python-3.9.5.tgz
yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel

mv Python-3.9.5.tgz ../librarys/Mac
cd ../librarys/Mac

tar zxvf Python-3.9.5.tgz

#./configure --prefix=$now_path