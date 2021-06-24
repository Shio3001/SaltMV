this=$(cd $(dirname $0);pwd)
now=$(cd $this;cd ../ ;pwd)

address="$now/librarys/Mac"
temp_path="$now/setup_mac_linux/temp"

rm -rv $address
mkdir $address

cd setup_mac_linux

echo $now
echo $address
echo $temp_path

mkdir temp

cd $address
#sh pysetup.sh $now $address $temp_path
sh "$this/boost.sh" $now $address $temp_path

rm -rv $temp_path


cd $now

