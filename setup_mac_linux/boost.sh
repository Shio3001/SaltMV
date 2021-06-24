address=$1
temp_path=$2

wget -P $temp_path https://boostorg.jfrog.io/artifactory/main/release/1.76.0/source/boost_1_76_0.tar.gz

tar zxvf "$temp_path/boost_1_76_0.tar.gz"
sh "$temp_path/bootstrap.sh"

mv -v boost_1_76_0 $address