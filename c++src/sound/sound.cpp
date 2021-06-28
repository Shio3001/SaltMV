#include <future>
#include <iostream>

using namespace std;

future<int> add(int a, int b) {
  int c = a + b;
  co_return c;
}

future<void> test() {
  int ret = co_await add(1, 2);
  cout << "return " << ret << endl;
}

int main() {
  auto fut = test();
  fut.wait();

  return 0;
}

/*https://cpprefjp.github.io/reference/future/future.html*/
/*https://qiita.com/sage-git/items/ffe463c0de05344d721b*/
