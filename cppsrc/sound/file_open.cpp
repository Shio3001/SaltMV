// 16ビット モノラル

#include <bits/stdc++.h>
#include <math.h>
using namespace std;
// g++ sample.cpp -framework OpenAL

class FileOpen {
 public:
  int main() {
    std::ifstream myfile("test.wav", std::ios::binary);

    if (!myfile.is_open()) {
      // not reading goes here
      return 0;
    }

    // myfile.seekg(0, std::ios_base::end);
    int file_size_len_sta = myfile.tellg();
    cout << file_size_len_sta << endl;

    myfile.seekg(0, std::ios::ios_base::end);
    int file_size_len = myfile.tellg();
    myfile.seekg(0);

    cout << file_size_len << endl;

    double compression_rate;
    myfile.read((char*)&compression_rate, sizeof(compression_rate));

    // As well as probably the sample rate...
    double sample_rate;
    myfile.read((char*)&sample_rate, sizeof(sample_rate));

    int nb_samples;
    myfile.read((char*)&nb_samples, sizeof(nb_samples));

    vector<double> vect;
    vect.resize(nb_samples);
    myfile.read((char*)&vect[0], nb_samples * sizeof(double));

    cout << compression_rate << endl;
    cout << sample_rate << endl;
    cout << nb_samples << endl;
    cout << vect.size() << endl;

    myfile.seekg(44);

    int end = file_size_len;
    cout << end << endl;

    cout << "********" << endl;

    int po = 0;

    double d;                //文字列ではないデータ
    while (!myfile.eof()) {  //ファイルの最後まで続ける
      myfile.read((char*)&d, sizeof(double));
      //文字列ではないデータを読みこむ

      po++;
    }

    cout << po << endl;

    /*

    cout << file << endl;

    // RIFFチャンクの読み込み
    // FILE* file = nullptr;
    // RIFF riff = {};
    // fread_s(&riff, sizeof(riff), sizeof(riff), 1, file);

    double d;              //文字列ではないデータ
    while (!file.eof()) {  //ファイルの最後まで続ける
      file.read((char*)&d, sizeof(double));
      //文字列ではないデータを読みこむ
      cout << d << endl;
    }

    */

    /*
std::ifstream ifs("運行番号.wav", std::ios::binary);
if (!ifs) {
  return -1;
}                  //ファイルが開けたか確認
char buffer[256];  // 256バイト分のバッファ
ifs.read(buffer, 256);  //ストリームから256バイトバッファに読み込む
std::cout.write(buffer, 256);  //標準出力に出力してみる
*/
    return 0;
  }
};

int main() {
  FileOpen fileopen;
  fileopen.main();
}

// 音声処理に関する参考文献一覧
// http://www.kk.iij4u.or.jp/~kondo/wave/
// http://gurigumi.s349.xrea.com/programming/binary.html
// https://okwave.jp/qa/q2310857.html
// http://www.na.scitec.kobe-u.ac.jp/~yaguchi/project-a-24/wav.htm
// https://tomosoft.jp/design/?p=40796 ← これpyだったわ
// https://art-of-life.jp/posts/wave/
// https://www.youtube.com/watch?v=rHqkeLxAsTc ← すごく良い動画だけど英語

// https://gist.github.com/tkaczenko/21ced83c69e30cfbc82b
//どっかで見つけたコード

// https://stackoverflow.com/questions/16075233/reading-and-processing-wav-file-data-in-c-c
// 英語わからん

// http://soundfile.sapp.org/doc/WaveFormat/
//どっかの大学の記事らしい

// https://teratail.com/questions/324485
// これ良さそう・・・？

// https://necotech.org/archives/657
// これが結局良さそう ←2度目

// https://www.youtube.com/watch?v=YIdgeuEjZoE
// ああ

// https://base64.work/so/c%2B%2B/2790291
// おおおお

// https://cpprefjp.github.io/reference/istream/basic_istream/seekg.html
// seekg

// https://so-zou.jp/software/tech/programming/cpp/run-time-library/stream/file.htm#no5
// ファイルの読み込みについて

// 香川行ってうどん食べた〜〜〜〜い！瀬戸内海を感じたい〜〜〜〜〜〜〜〜〜〜！
// おふねしたい

// https://ferry.co.jp/
// おふね