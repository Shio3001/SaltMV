now=$1
address=$2
temp_path=$3

wget -P $temp_path https://github.com/Shio3001/KonanMV/archive/refs/heads/release.zip
#KonanMV-release.zip

tar zxvf "$temp_path/KonanMV-release.zip"
#sh "$temp_path/bootstrap.sh"

