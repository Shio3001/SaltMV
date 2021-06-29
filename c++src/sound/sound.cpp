// 16ビット モノラル

#include <AL/alut.h>
#include <bits/stdc++.h>
#include <math.h>
using namespace std;
// g++ sample.cpp -framework OpenAL

class SoundManagement {
  int sta() {
    // OpenALの下準備　おまじない的な
    ALCdevice *device = alcOpenDevice(NULL);
    ALCcontext *context = alcCreateContext(device, NULL);
    alcMakeContextCurrent(context);

    //バッファ(保存領域)とソース(音源)を宣言
    ALuint buffer;
    ALuint source;
    //それを生成
    alGenBuffers(1, &buffer);
    alGenSources(1, &source);
  }
  int sound() {
    //ここにサウンド関連の処理を記述していくんじゃ
    return 0;
  }
  int end() {
    alcMakeContextCurrent(nullptr);
    alcDestroyContext(context);
    alcCloseDevice(device);
    return 0;
  }
};

// https://hatakenoko.hateblo.jp/entry/2018/05/24/220046
