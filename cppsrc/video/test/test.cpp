// 16ビット モノラル
#include <bits/stdc++.h>
#include <math.h>

#include <boost/python.hpp>
using namespace std;
using namespace boost::python;

class World {
 public:
  World() { cout << "ya~~~~~~~~~i omaenchi boroyashiki" << endl; }

  // void Tokushima(std::string a) { cout << b << endl; }

  void hoge(std::string b) { cout << b << endl; }
  void hage(std::string c) { cout << c << endl; }
};

BOOST_PYTHON_MODULE(test) {
  class_<World>("World", init<>())
      //.def("__init__", make_constructor(&World::initWrapper))
      .def("hoge", &World::hoge)
      .def("hage", &World::hage);
}

// https://stackoverflow.com/questions/54708598/is-this-boostpython-python-3-7-error-init-should-return-none-not-no
// https://qiita.com/funabashi800/items/c13c4f742f43d9ebdd86
// Nonetypeを返すなって怒られた時は

// class_<World>("World", init<>()) ←initの引数がない時に指定