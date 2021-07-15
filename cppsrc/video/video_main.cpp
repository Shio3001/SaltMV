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

namespace EffectProgress
{
  class EffectProduction
  {
    void effect_group()
    {
    }
    void effect_individual()
    {
    }
  };
}

namespace ObjectProgress
{
  namespace EP = EffectProgress;
  class ObjectProduction
  {
    void object_group()
    {
    }
    void object_individual()
    {
      EP::EffectProduction *effect_production = new EP::EffectProduction();
      delete effect_production;
    }
  };
}
namespace VideoMain
{
  class VideoExecutionCenter
  {
    py::object scene;
    py::dict editor;
    py::dict out_func;
    py::dict python_operation;
    py::object video_image_control;

  public:
    VideoExecutionCenter(py::dict send_operation, py::object send_scene, py::dict send_out_func)
    {
      // editor["x"] = extract<int>(x);
      // editor["y"] = extract<int>(y);
      // editor["fps"] = extract<int>(fps);
      // editor["frame"] = extract<int>(frame);

      scene = send_scene;
      editor(send_scene.attr("editor"));
      out_func = send_out_func;

      python_operation = send_operation;
      video_image_control = python_operation["video_image"];

      //EffectProduction effect_production;

      //cout << editor["x"] << editor["y"] << editor["fps"] << editor["frame"] << endl;
    }

    void execution_main()
    {
    }

    void execution_preview()
    {
    }

  private:
    //np::ndarray
    void run()
    {
      namespace OP = ObjectProgress;
      OP::ObjectProduction *object_production = new OP::ObjectProduction();
      delete object_production;
    }
  };
}

BOOST_PYTHON_MODULE(video_main)
{
  py::class_<VideoMain::VideoExecutionCenter>("VideoExecutionCenter",
                                              py::init<py::dict, py::object, py::dict>())
      //.def("sta", &VideoExecutionCenter::sta)
      .def("execution_main", &VideoMain::VideoExecutionCenter::execution_main)
      .def("execution_preview", &VideoMain::VideoExecutionCenter::execution_preview);
  //.def("sta", &VideoExecutionCenter::sta)
  //.def("execution", &VideoExecutionCenter::execution)
  //.def("layer_interpretation", &VideoExecutionCenter::layer_interpretation);
}

/*
BOOST_PYTHON_MODULE(video_main) {
  def("init", &video_execution_center.init);
  def("execution", &video_execution_center.execution);
}*/

// https://base64.work/so/python/1904052
// http://alpha.osdn.jp/devel/boost.python_ja.pdf

// https://moriyoshi.hatenablog.com/entry/20091214/1260779899

// https://yokaze.github.io/boost-python-lookup/import.html python module import
// について

// https://marycore.jp/programmer/c-lang-is-lorry/