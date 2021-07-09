// 16ビット モノラル
#include <bits/stdc++.h>
#include <math.h>
#include <stdio.h>

#include <boost/python.hpp>
#include <boost/python/numpy.hpp>
#include <iomanip>
using namespace std;
namespace py = boost::python;
namespace np = boost::numpy;

class VideoExecutionCenter {
 private:
  map<string, int> editor;
  py::dict python_operation;

 public:
  void sta(py::dict operation, int x, int y, int fps, int frame) {
    // editor["x"] = extract<int>(x);
    // editor["y"] = extract<int>(y);
    // editor["fps"] = extract<int>(fps);
    // editor["frame"] = extract<int>(frame);

    editor["x"] = x;
    editor["y"] = y;
    editor["fps"] = fps;
    editor["frame"] = frame;

    python_operation = operation;

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

    py::list object_group_values(object_group.values());
    py::list layer_layer_id_values(layer_layer_id.values());

    int object_group_len = py::len(object_group);
    cout << "object_group_len" << object_group_len << endl;

    py::object sy(python_operation["synthetic"].attr("call"));
    sy("test");

    // for (i = 0; i < object_group_len; i++) {
    //  object_group_values[i]
    //}

    // py::list object_group_keys(object_group.attr("keys"));
    // py::list layer_layer_id_keys(layer_layer_id.attr("keys"));
  }

 private:
  void layer_interpretation() {}
  void group_object(py::list object_group, int object_group_len) {
    for (int i = 0; i < object_group_len; i++) {
      py::object media_object(object_group[i]);
      object_individual(media_object);
    }
  }

  void object_individual(py::object media_object) {}

  void group_effect() {}

  void effect_individual() {}

  int[] now_currently_midpoint() {
    int now_
    return
  }
};

BOOST_PYTHON_MODULE(video_main) {
  py::class_<VideoExecutionCenter>("VideoExecutionCenter")
      .def("sta", &VideoExecutionCenter::sta)
      .def("execution", &VideoExecutionCenter::execution);
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