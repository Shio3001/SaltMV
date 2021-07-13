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

class VideoExecutionCenter
{
private:
  map<string, int> editor;
  py::dict python_operation;
  py::object video_image_control;
  np::ndarray draw_base; //全体のキューも兼ねている
  py::dict object_group;
  py::dict layer_layer_id;
  py::list object_group_keys;
  py::list layer_layer_id_keys;
  py::list object_group_values;
  py::list layer_layer_id_values;

public:
  VideoExecutionCenter(py::dict operation, int x, int y, int fps, int frame)
  {
    // editor["x"] = extract<int>(x);
    // editor["y"] = extract<int>(y);
    // editor["fps"] = extract<int>(fps);
    // editor["frame"] = extract<int>(frame);

    editor["x"] = x;
    editor["y"] = y;
    editor["fps"] = fps;
    editor["frame"] = frame;

    python_operation = operation;
    video_image_control = python_operation["video_image"].attr("Control_Video_Image")();

    draw_base = np::zeros((editor["frame"], editor["y"], editor["x"], 4));

    cout << editor["x"] << editor["y"] << editor["fps"] << editor["frame"] << endl;
  }
  void execution_preview(py::object scene)
  {
    int now_frame = (int)py::extract<double>(scene.attr("now_time"));
    //mp4なりのファイルに書き出しをしない
    //フレーム指定が-1以外の場合、
    //非同期処理必要そう

    init_objcet_list(now_frame);
  }

  void execution(py::object scene)
  {
    cout << "ここから execution" << endl;
    cout << py::extract<double>(scene.attr("now_time")) << endl;

    //int now_frame = (int)py::extract<double>(scene.attr("now_time"));

    init_objcet_list();
  }

  void init_objcet_list(int frame = -1)
  {

    string scene_id = py::extract<string>(scene.attr("scene_id"));
    cout << scene_id << endl;

    py::object layer_group(scene.attr("layer_group"));
    object_group(layer_group.attr("object_group"));
    layer_layer_id(layer_group.attr("layer_layer_id"));

    object_group_keys(object_group.keys());
    layer_layer_id_keys(layer_layer_id.keys());

    object_group_values(object_group.values());
    layer_layer_id_values(layer_layer_id.values());

    if (frame == -1)
    {
      int out_sta = 0;
      int out_end = editor["frame"];

      for (int i = out_sta; i < out_end; i++)
      {
        draw_base[i] = frame_pass(i);
      }
    }
    else
    {
      draw_base[frame] = frame_pass(frame);
    }
  }

  np::ndarray frame_pass(int frame)
  {

    int layer_len = py::len(layer_layer_id_keys);
    group_object(object_group_values, layer_layer_id, layer_len, frame);

    // for (i = 0; i < object_group_len; i++) {
    //  object_group_values[i]
    //}

    // py::list object_group_keys(object_group.attr("keys"));
    // py::list layer_layer_id_keys(layer_layer_id.attr("keys"));
  }

private:
  np::ndarray layer_interpretation() {}
  np::ndarray group_object(py::list object_group, py::dict layer_layer_id,
                           int layer_len, int now_frame)
  {
    int object_group_len = py::len(object_group);
    cout << "object_group_len" << object_group_len << endl;
    //object[layer_len] object_group_procedure;
    map<int, py::object> object_group_procedure;
    vector<int> object_group_procedure_key;
    for (int i = 0; i < object_group_len; i++)
    {
      py::object installation = object_group[i][0].attr("installation");

      int sta = py::extract<int>(installation[0]);
      int end = py::extract<int>(installation[1]);

      if (!(sta <= now_frame < end))
      {
        cout << "時間外のため退去" << endl;
        continue;
      }

      py::object object_group_obj = object_group[i][1];
      string layer_id = py::extract<string>(object_group_obj);
      py::object now_layer_obj = layer_layer_id[layer_id]; //str->int
      int now_layer = py::extract<int>(now_layer_obj);
      object_group_procedure[now_layer] = object_group[i][0];
      object_group_procedure_key.push_back(now_layer);
    }

    sort(object_group_procedure_key.begin(), object_group_procedure_key.end()); // vector
    //numbers.erase(unique(numbers.begin(), numbers.end()), numbers.end());

    //ここから本ループ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    for (int j = 0; j < object_group_procedure_key.size(); j++)
    {
      int now_nun = object_group_procedure_key[j];
      py::object now_obj = object_group_procedure[now_nun];
      py::object media_object(now_obj);

      string synthetic_type = now_obj.attr("synthetic");
      np::ndarray obj_substance = object_individual(media_object);

      py::object synthetic_func(python_operation["synthetic"].attr("call"));

      np::ndarray now_draw = draw_base[now_frame];
      np::ndarray synthesized = synthetic_func(synthetic_type, now_draw, obj_substance);

      draw_base[now_frame] = synthesized;
    }
  }

  void object_individual(py::object media_object)
  {
    np::ndarray now_base = np::zeros((editor["y"], editor["x"], 4));

    py::object installation = media_object.attr("installation");
    int sta = py::extract<int>(installation[0]);
    int end = py::extract<int>(installation[1]);

    py::object effect_group = media_object.attr("effect_group");
    group_effect(effect_group, sta, end)
  }

  np::ndarray group_effect(py::list media_obj_group, int sta, int end)
  {
    int media_obj_group_len = py::len(media_obj_group);
    for (int i = 0; i < media_obj_group_len; i++)
    {
      py::object media_obj_object(media_obj_group[i]);
      effect_individual(media_obj_object);
    }
  }

  np::ndarray effect_individual(py::object layer_object) {}

  void now_currently_midpoint() {}
};

BOOST_PYTHON_MODULE(video_main)
{
  py::class_<VideoExecutionCenter>("VideoExecutionCenter",
                                   py::init<py::dict, int, int, int, int>())
      //.def("sta", &VideoExecutionCenter::sta)
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

// https://marycore.jp/programmer/c-lang-is-lorry/