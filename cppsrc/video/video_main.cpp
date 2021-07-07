// 16ビット モノラル
#include <bits/stdc++.h>
#include <math.h>
#include <stdio.h>

#include <boost/python.hpp>
#include <iomanip>
using namespace std;
using namespace boost::python;

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
  void execution(object scene) {
    cout << extract<double>(scene.attr("now_time")) << endl;
    object layer_group = scene.attr("layer_group");
    dict object_group(layer_group.attr("object_group"));
    dict layer_layer_id(layer_group.attr("layer_layer_id"));
  }
  void layer_interpretation() {}
};

BOOST_PYTHON_MODULE(video_main) {
  class_<VideoExecutionCenter>("VideoExecutionCenter")
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