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

namespace AudioProgress
{
    class AudioNumpyProgress
    {
        public:
        AudioNumpyProgress()
        {
        }
        np::ndarray upsampling(np::ndarray &principal, int up_rate)
        {
            int principal_len = py::extract<py::int>(py::len(principal));
            shape_size = principal_len * up_rate;
            np::ndarray new_base = np::zeros(shape_size, np::dtype::get_builtin<uint>());

            int pattern = -1 * (up_rate-1);
            new_base[::pattern] = principal;
            return;
        }
        np::ndarray downsampling(np::ndarray &principal, int down_rate)
        {
            int principal_len = py::extract<py::int>(py::len(principal));

            int pattern = -1 * (up_rate-1);
            np::ndarray new_base = np::delete(principal, pattern, 0)
            return;
        }
    };
}

BOOST_PYTHON_MODULE(video_main)
{
    Py_Initialize();
    np::initialize();
    py::class_<AudioProgress::AudioNumpyProgress>("AudioNumpyProgress")

        //.def("sta", &VideoExecutionCenter::sta)
        .def("upsampling", &AudioProgress::AudioNumpyProgress::upsampling)
        .def("downsampling", &AudioProgress::AudioNumpyProgress::downsampling);
    //.def("sta", &VideoExecutionCenter::sta)
    //.def("execution", &VideoExecutionCenter::execution)
    //.def("layer_interpretation", &VideoExecutionCenter::layer_interpretation);
}