// 16ビット モノラル

#include <bits/stdc++.h>
#include <math.h>
#include <stdio.h>
using namespace std;

int main() {
  // 読み込みファイル名
  std::string filepath = "test.wav";

  // ifstreamを使って読み込みます
  std::ifstream wavfile(filepath, std::ios::binary);

  // ファイルが空いているかどうかを確認します
  if (!wavfile.is_open()) {
    return 0;
  }

  char riff[4];
  uint chunk_size;
  char format[4];
  char sub_chunk_id[4];
  uint sub_chunk_size;
  uint audio_format;
  uint numchannel;
  uint sample_rate;
  uint byte_rate;
  uint block_align;
  uint bits_per_sample;
  char sub_chunk_size_id_second[4];
  uint sub_chunk_size_suze_second;

  wavfile.seekg(0);
  wavfile.read((char*)&riff, 4);
  cout << riff << endl;

  wavfile.seekg(4);
  wavfile.read((char*)&chunk_size, 4);
  cout << chunk_size << endl;

  wavfile.seekg(8);
  wavfile.read((char*)&format, 4);
  cout << format << endl;

  wavfile.seekg(12);
  wavfile.read((char*)&sub_chunk_id, 4);
  cout << sub_chunk_id << endl;

  wavfile.seekg(16);
  wavfile.read((char*)&sub_chunk_size, 4);
  cout << sub_chunk_size << endl;

  wavfile.seekg(20);
  wavfile.read((char*)&audio_format, 2);
  cout << audio_format << endl;

  wavfile.seekg(22);
  wavfile.read((char*)&numchannel, 2);
  cout << numchannel << endl;

  wavfile.seekg(24);
  wavfile.read((char*)&sample_rate, 4);
  cout << sample_rate << endl;

  wavfile.seekg(28);
  wavfile.read((char*)&byte_rate, 4);
  cout << byte_rate << endl;

  wavfile.seekg(32);
  wavfile.read((char*)&block_align, 2);
  cout << block_align << endl;

  wavfile.seekg(34);
  wavfile.read((char*)&bits_per_sample, 2);
  cout << bits_per_sample << endl;

  wavfile.seekg(36);
  wavfile.read((char*)&sub_chunk_size_id_second, 4);
  cout << sub_chunk_size_id_second << endl;

  wavfile.seekg(40);
  wavfile.read((char*)&sub_chunk_size_suze_second, 4);
  cout << sub_chunk_size_suze_second << endl;

  wavfile.seekg(44);
  //波形データを格納。リニアPCMの場合は時間順に格納される。ステレオは左→右→左→右…のように格納される。8ビットの場合は符号無し整数
  //(0 – 255)、16ビットの場合は符号付き整数 (-32768 – 32767) で表わす。
  int chunk_len = sub_chunk_size / sub_chunk_size;
  cout << chunk_len << endl;

  // http://www.ys-labo.com/pc/2009/091223%20File.html
  // http://soundfile.sapp.org/doc/WaveFormat/
  // https://taku-o.hatenablog.jp/entry/20181120/1542726865
  // https://www.youfit.co.jp/archives/1418 ←対応表 有能くん
}