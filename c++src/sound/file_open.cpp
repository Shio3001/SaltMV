// 16ビット モノラル

#include <bits/stdc++.h>
#include <math.h>
using namespace std;
// g++ sample.cpp -framework OpenAL

class FileOpen {
 public:
  int main() {
    std::ifstream ifs("test.wav", std::ios::binary);

    cout << ifs << endl;

    double d;             //文字列ではないデータ
    while (!ifs.eof()) {  //ファイルの最後まで続ける
      ifs.read((char*)&d, sizeof(double));
      //文字列ではないデータを読みこむ
      cout << d << endl;
    }
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

// http://www.kk.iij4u.or.jp/~kondo/wave/
// http://gurigumi.s349.xrea.com/programming/binary.html
// https://okwave.jp/qa/q2310857.html
// http://www.na.scitec.kobe-u.ac.jp/~yaguchi/project-a-24/wav.htm
// https://tomosoft.jp/design/?p=40796 ← これpyだったわ
