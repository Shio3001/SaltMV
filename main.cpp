
#include <bits/stdc++.h>
using namespace std;
namespace py = boost::python;
int main() {
  /*std::system(
      "librarys/Mac/Python-3.9.5/bin/NankokuMovieMaker pysrc/main_py.py");*/
  py::Py_Initialize();  // 最初に呼んでおく必要あり

  try {
    // Pythonで「print('Hello World!')」を実行
    py::object global = py::import("main_py");
    py::exec("main_py()", global);
  } catch (const py::error_already_set &) {
    // Pythonコードの実行中にエラーが発生した場合はエラー内容を表示
    py::PyErr_Print();
  }
  return 0;
}

// /Users/"私の名前"/boost_build
// find librarys/Mac -name pyconfig.h
//"compilerPath": "/usr/local/Cellar/gcc/10.2.0/bin/gcc-10", にしたら# include
//<pyconfig.h>なおった