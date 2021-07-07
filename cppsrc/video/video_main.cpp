// 16ビット モノラル
#include <bits/stdc++.h>
#include <math.h>
#include <stdio.h>

#include <boost/python.hpp>
#include <iomanip>
using namespace std;
namespace py = boost::python;

class VideoExecutionCenter {
 private:
  map<string, int> editor;

 public:
  void sta(int x, int y, int fps, int frame) {
    // editor["x"] = extract<int>(x);
    // editor["y"] = extract<int>(y);
    // editor["fps"] = extract<int>(fps);
    // editor["frame"] = extract<int>(frame);

    editor["x"] = x;
    editor["y"] = y;
    editor["fps"] = fps;
    editor["frame"] = frame;

    cout << editor["x"] << editor["y"] << editor["fps"] << editor["frame"]
         << endl;
  }
  void execution(py::object scene) {
    cout << "ここから execution" << endl;
    cout << py::extract<double>(scene.attr("now_time")) << endl;

    string scene_id = py::extract<string>(scene.attr("scene_id"));
    cout << scene_id << endl;

    py::object layer_group(scene.attr("layer_group"));
    py::dict object_group(layer_group.attr("object_group"));
    py::dict layer_layer_id(layer_group.attr("layer_layer_id"));

    py::list object_group_keys(object_group.keys());
    py::list layer_layer_id_keys(layer_layer_id.keys());

    int len_test = py::len(object_group);
    cout << "len_test" << len_test << endl;

    // py::list object_group_keys(object_group.attr("keys"));
    // py::list layer_layer_id_keys(layer_layer_id.attr("keys"));
  }
  void layer_interpretation() {}
};

BOOST_PYTHON_MODULE(video_main) {
  py::class_<VideoExecutionCenter>("VideoExecutionCenter")
      .def("sta", &VideoExecutionCenter::sta)
      .def("execution", &VideoExecutionCenter::execution)
      .def("layer_interpretation", &VideoExecutionCenter::layer_interpretation);
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