#include <boost/python.hpp>
#include <iostream>
using namespace boost::python;
using namespace std;

string f(string text) {
  cout << "B1" << endl;
  cout << text << endl;
  cout << "B2" << endl;
  return text + " ←いいね";
}

BOOST_PYTHON_MODULE(test2) { def("f", &f); }
