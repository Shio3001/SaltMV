// 16ビット モノラル
#include <bits/stdc++.h>
#include <math.h>
#include <stdio.h>

#include <boost/python.hpp>
#include <iomanip>
using namespace std;
namespace py = boost::python;

class CppEffectLord {
  object main() {}

  BOOST_PYTHON_MODULE(cpp_effect_lord){
      py::class_<CppEffectLord>("CppEffectLord")
          .def("main", &CppEffectLord::main);
};

  class Manage {};
