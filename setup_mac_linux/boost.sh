now=$1
address=$2
temp_path=$3

mkdir $address/1_76_0/
cd $address/1_76_0/
#wget https://boostorg.jfrog.io/artifactory/main/release/1.76.0/source/boost_1_76_0.tar.gz
#tar zxvf boost_1_76_0.tar.gz

echo "[ 終了 ] boost download"
cd boost_1_76_0
echo "[ 開始 ] ./bootstrap.sh"
./bootstrap.sh
echo "[ 終了 ] ./bootstrap.sh"
echo "[ 開始 ] ./b2"
./b2 --prefix=$address/1_76_0/ --cmd-or-prefix=$address/Python-3.9.5/bin/python3.9 --includes=$address/Python-3.9.5/include/python3.9/
echo "[ 終了 ] ./b2"
#./b2 install -j2 --prefix=$address/1_76_0/ --with-python=$address/Python-3.9.5/bin/python3.9 
#./bootstrap.sh --with-libraries=python --with-python=python3 --with-python-version=3.9
#NankokuMovieMaker/librarys/Mac/Python-3.9.5/bin/python3.9
#$address/Python-3.9.5/include
cd $address

#ls | grep
#g++ -Wall -O2 -fpic `/Users/maruyama/Programs/MVproject/NankokuMovieMaker/librarys/Mac/Python-3.9.5/bin/python3.9-config --include` -c main.cpp
#g++ -shared -o main.so `/Users/maruyama/Programs/MVproject/NankokuMovieMaker/librarys/Mac/Python-3.9.5/bin/python3.9-config --ldflags` -lboost_python main.o