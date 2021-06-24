now=$1
address=$2
temp_path=$3

wget -P $temp_path https://boostorg.jfrog.io/artifactory/main/release/1.76.0/source/boost_1_76_0.tar.gz

tar zxvf "$temp_path/boost_1_76_0.tar.gz"


cd "$temp_path/boost_1_76_0"
./bootstrap.sh
./bjam --prefix=$address
./b2 install -j2 --prefix=$address
cd $address
