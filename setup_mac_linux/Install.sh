now=$(pwd)
address="$now/librarys/Mac"
temp_path="$now/setup_mac_linux/temp"

cd setup_mac_linux

echo $now
echo $address
echo $temp_path

mkdir temp
sh boost.sh $address $temp_path
cd $now