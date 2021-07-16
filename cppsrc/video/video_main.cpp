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
  public:
    py::dict effect_group;
    py::dict py_out_func;
    py::dict python_operation;
    py::object video_image_control;
    EffectProduction(py::dict &send_effect_group, py::dict &send_py_out_func, py::dict &send_python_operation, py::object &send_video_image_control)
    {
      effect_group = send_effect_group;
      py_out_func = send_py_out_func;
      python_operation = send_python_operation;
      video_image_control = send_video_image_control;
    }
    void production_effect_group()
    {
      int effect_len = py::len(effect_group);

      for (i = 0; i < effect_len; i++)
      {
        production_effect_individual(effect_group[i])
      }
    }
    void production_effect_individual(py::object effect)
    {
    }
  };
}

namespace ObjectProgress
{
  namespace EP = EffectProgress;
  class ObjectProduction
  {
  public:
    int frame;

    py::dict py_out_func;
    py::dict python_operation;
    py::object video_image_control;
    py::dict object_group;
    py::dict layer_layer_id;
    map<int, py::object> order_decision_object_group;
    vector<int> order_decision_object_group_number;

    int object_len;

    ObjectProduction(int send_frame, py::dict &send_object_group, py::dict &send_layer_layer_id, py::dict &send_py_out_func, py::dict &send_python_operation, py::object &send_video_image_control)
    {
      frame = send_frame;
      object_group = send_object_group;
      layer_layer_id = send_layer_layer_id;
      py_out_func = send_py_out_func;
      python_operation = send_python_operation;
      video_image_control = send_video_image_control;
      object_len = py::len(object_group);
    }

    void production_order_decision()
    {
      for (int i = 0; i < object_len; i++)
      {

        py::object this_object = py::list(object_group.values())[i];
        py::list installation = py::extract<py::list>(this_object[0].attr("installation"));

        bool low = py::extract<int>(installation[0]) < frame;
        bool high = frame < py::extract<int>(installation[1]);

        bool low_high_scope = low * high;

        if (low_high_scope)
        {
          string layer_id = py::extract<string>(this_object[1]);

          py::object layer_number_func = py_out_func["layer_number"];

          int now_layer_number = py::extract<int>(layer_number_func(layer_id));

          order_decision_object_group[now_layer_number] = this_object[0];

          order_decision_object_group_number.push_back(now_layer_number);

          cout << "frame" << frame << " / now_layer_number " << now_layer_number << " / installation " << py::extract<int>(installation[0]) << " " << py::extract<int>(installation[1]) << " " << endl;
        }
      }
    }
    sort(order_decision_object_group_number.begin(), order_decision_object_group_number.end()); // vector

    void production_object_group()
    {
      for (int i = 0; i < order_decision_object_group_number.size(); i++)
      {
        int now_object_nun = order_decision_object_group_number[i];
        py::object now_objcet = order_decision_object_group[now_object_nun];

        production_object_individual(now_objcet)
      }
    }

    void production_object_individual(py::object &now_objcet)
    {
      py::dict effect_group = now_objcet.attr("effect_point");

      EP::EffectProduction *effect_production = new EP::EffectProduction(effect_group, py_out_func, python_operation, video_image_control);
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
    py::dict py_out_func;
    py::dict python_operation;
    py::object video_image_control;

    py::object layer_group;
    py::dict object_group;
    py::dict layer_layer_id;

  public:
    VideoExecutionCenter(py::dict send_operation, py::object send_scene, py::dict send_py_out_func)
    {
      // editor["x"] = extract<int>(x);
      // editor["y"] = extract<int>(y);
      // editor["fps"] = extract<int>(fps);
      // editor["frame"] = extract<int>(frame);

      scene = send_scene;
      layer_group = py::extract<py::object>(scene.attr("layer_group"));
      object_group = py::extract<py::dict>(layer_group.attr("object_group"));
      layer_layer_id = py::extract<py::dict>(layer_group.attr("layer_layer_id"));

      editor = py::extract<py::dict>(send_scene.attr("editor"));
      py_out_func = send_py_out_func;
      python_operation = send_operation;
      video_image_control = python_operation["video_image"];

      //EffectProduction effect_production;

      //cout << editor["x"] << editor["y"] << editor["fps"] << editor["frame"] << endl;
    }

    void execution_main(int sta = -1, int end = -1)
    {
      if (sta == -1)
      {
        sta = 0;
      }
      if (end == -1)
      {
        end = py::extract<int>(editor["len"]);
      }

      for (int i = sta; i < end; i++)
      {
        run(i);
      }
    }

    void execution_preview(int frame)
    {
      if (frame > py::extract<int>(editor["len"]))
      {
        frame = py::extract<int>(editor["len"]);
      }

      run(frame);
    }

  private:
    //np::ndarray
    void run(int frame)
    {
      namespace OP = ObjectProgress;
      OP::ObjectProduction *object_production = new OP::ObjectProduction(frame, object_group, layer_layer_id, py_out_func, python_operation, video_image_control);

      object_production->production_order_decision();

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

//https://qiita.com/ur_kinsk/items/949dabe975bdc1affb82