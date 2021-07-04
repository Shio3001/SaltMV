// 16ビット モノラル

#include <bits/stdc++.h>
#include <math.h>
using namespace std;

int main() {
  // ファイルを開ける
  string filepath = "test.wav";
  FILE* file = NULL;
  _tfopen_s(&file, filepath, _T("rb"));

  // RIFF Chunkを読み込む
  RiffChunk riff;
  fread(&riff, sizeof(RiffChunk), 1, file);

  // RIFF Chunkのtagが「RIFF」以外の場合、フォーマットエラーとみなす
  if (strncmp(riff.head.id, "RIFF", 4) != 0) {
    fclose(file);
    return 0;
  }

  // RIFF Chunkのformatが「WAVE」以外の場合、フォーマットエラーとする
  if (strncmp(riff.format, "WAVE", 4) != 0) {
    fclose(file);
    return 0;
  }

  ChunkHead chunk;

  while (!feof(file)) {
    // 一つのChunkHeadを読み込む
    ZeroMemory(&chunk, sizeof(ChunkHead));
    fread(&chunk, sizeof(ChunkHead), 1, file);

    // Chunkのサイズが0より小さい場合エラーとする
    // （ファイルフォーマットが正しくない場合）
    if (chunk.size < 0) break;

    if (strncmp(chunk.id, "fmt ", 4) == 0) {
      // Wave Format Chunkを読み込み
      WaveFileFormat format;
      fread(&format, min(chunk.size, sizeof(WaveFileFormat)), 1, file);

      // 先頭6つの要素以外の要素があれば、そのデータを無視してカーソルを移動させる
      fseek(file, chunk.size - sizeof(WaveFileFormat), SEEK_CUR);
    } else if (strncmp(chunk.id, "data", 4) == 0) {
      // Waveのデータを読み込む
      char* buffer = new char[chunk.size];
      fread(buffer, chunk.size, 1, file);
    } else {
      // 認識できないChunkをSkipしてカーソルを移動させる
      fseek(file, chunk.size, SEEK_CUR);
    }
  }

  // ファイルを閉じる
  fclose(file);
  return 0;
}

// 参考
// https://necotech.org/archives/657