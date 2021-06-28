now=$1
address=$2
temp_path=$3

mkdir $address/1_76_0/
cd $address/1_76_0/
wget https://boostorg.jfrog.io/artifactory/main/release/1.76.0/source/boost_1_76_0.tar.gz
tar zxvf boost_1_76_0.tar.gz
cd boost_1_76_0
./bootstrap.sh
#./bjam --prefix=$address/1_76_0/
./b2 install -j2 --prefix=$address/1_76_0/ python=$address/Python-3.9.5/bin/python3.9
#NankokuMovieMaker/librarys/Mac/Python-3.9.5/bin/python3.9
cd $address
