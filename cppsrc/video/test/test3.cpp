// 16ビット モノラル
#include <bits/stdc++.h>
#include <math.h>
#include <stdio.h>

#include <boost/python.hpp>
#include <boost/python/numpy.hpp>
#include <iomanip>
using namespace std;
namespace py = boost::python;
namespace np = boost::python::numpy;

void test()
{
    cout << " いいね " << endl;
}

BOOST_PYTHON_MODULE(test3)
{
    Py_Initialize();
    np::initialize();
    //py::class_<TestNp>("TestNp", py::init<>())
    //.def("sta", &VideoExecutionCenter::sta)
    py::def("test", &test);
    //.def("sta", &VideoExecutionCenter::sta)
    //.def("execution", &VideoExecutionCenter::execution)
    //.def("layer_interpretation", &VideoExecutionCenter::layer_interpretation);
}
