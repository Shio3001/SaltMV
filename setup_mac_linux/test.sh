this=$(cd $(dirname $0);pwd)
now=$(cd $this;cd ../ ;pwd)

address="$now/librarys/Mac"
temp_path="$now/setup_mac_linux/temp"
sh "$temp_path/bjam"

####

wget https://boostorg.jfrog.io/artifactory/main/release/1.76.0/source/boost_1_76_0.tar.gz
tar xzf boost_1_76_0.tar.gz
cd boost_1_76_0
./bootstrap.sh
mkdir  boost_1_76_0
./b2 install -j2 --prefix=boost_1_76_0
