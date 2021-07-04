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
  wavfile.read((char*)&riff, 4);
  cout << riff << endl;
  // 0

  uint chunk_size;
  wavfile.read((char*)&chunk_size, 4);
  cout << chunk_size << endl;

  char format[4];
  wavfile.read((char*)&format, 4);
  cout << format << endl;

  char sub_chunk_id[4];
  wavfile.read((char*)&sub_chunk_id, 4);
  cout << sub_chunk_id << endl;

  uint sub_chunk_size;
  wavfile.read((char*)&sub_chunk_size, 4);
  cout << sub_chunk_size << endl;

  uint audio_format;
  wavfile.read((char*)&audio_format, 2);
  cout << audio_format << endl;

  uint numchannel;
  wavfile.read((char*)&numchannel, 2);
  cout << numchannel << endl;

  uint sample_rate;
  wavfile.read((char*)&sample_rate, 4);
  cout << sample_rate << endl;

  uint byte_rate;
  wavfile.read((char*)&byte_rate, 4);
  cout << byte_rate << endl;

  uint block_align;
  wavfile.read((char*)&block_align, 2);
  cout << block_align << endl;

  char bits_per_sample;
  wavfile.read((char*)&bits_per_sample, 2);
  cout << bits_per_sample << endl;
  // http://www.ys-labo.com/pc/2009/091223%20File.html
  // http://soundfile.sapp.org/doc/WaveFormat/
  // https://taku-o.hatenablog.jp/entry/20181120/1542726865
}