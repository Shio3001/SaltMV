
#include <bits/stdc++.h>

#include <boost/python.hpp>
namespace py = boost::python;
using namespace std;

int main() {
  Py_Initialize();
  try {
    // Pythonで「print('Hello World!')」を実行
    py::object global = py::import("__main__").attr("__dict__");
    py::exec_file("main_py.py", global);
  } catch (const py::error_already_set &) {
    // Pythonコードの実行中にエラーが発生した場合はエラー内容を表示
    PyErr_Print();
  }

  return 0;
}