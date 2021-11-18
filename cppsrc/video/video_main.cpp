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
//#include "synthetic.hpp"

#include "video_effect.hpp"
#include "video_object.hpp"
//synthetic_class["normal"] = synthetic_normal;

/*
namespace EffectProgressPlugin
{
  class EffectPluginElements
  {
    np::ndarray draw;
    EffectPluginElements(np::ndarray send_draw, py::dict send_effect_value, py::dict send_before_value, py::dict send_next_value, py::dict send_various_fixed, int send_now_frame, py::dict send_editor)
    {
      draw = send_draw;
      send_effect_value;
    }
  }
}*/

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
    py::object object_group;
    py::dict layer_layer_id;

  public:
    VideoExecutionCenter(py::dict send_operation, py::dict send_py_out_func)
    {
      // editor["x"] = extract<int>(x);
      // editor["y"] = extract<int>(y);
      // editor["fps"] = extract<int>(fps);
      // editor["frame"] = extract<int>(frame);

      py_out_func = send_py_out_func;
      python_operation = send_operation;
      video_image_control = python_operation["video_image"];

      //EffectProduction effect_production;

      ////cout << editor["x"] << editor["y"] << editor["fps"] << editor["frame"] << endl;
    }

    void scene_setup(py::object &send_scene)
    {
      scene = send_scene;
      editor = py::extract<py::dict>(send_scene.attr("editor"));
      layer_group = scene.attr("layer_group");
      object_group = layer_group.attr("object_group");
      layer_layer_id = py::extract<py::dict>(layer_group.attr("layer_layer_id"));
    }

    np::ndarray execution_main(int frame)
    {
      //vector<np::ndarray> draw_vector;

      cout << "execution_main 出力処理" << endl;

      int maxlen = py::extract<double>(editor["len"]);

      if (frame < 0)
      {
        frame = 0;
      }
      if (frame > maxlen)
      {
        frame = maxlen;
      }

      np::ndarray draw = run(frame, "BGR");

      return draw;
    }

    np::ndarray execution_preview(int frame)
    {
      cout << "execution_preview 出力処理" << endl;

      if (frame > py::extract<double>(editor["len"]))
      {
        frame = py::extract<double>(editor["len"]);
      }

      np::ndarray draw = run(frame, "RGB");
      //np::ndarray draw2 = run(frame);
      return draw;
    }

    void execution_preview_queue_all_del()
    {
    }

    np::ndarray execution_preview_queue_numpy(int frame)
    {
    }

    np::ndarray execution_preview_queue_tkinter(int frame)
    {
    }

    py::object object_group_recovery()
    {
      return object_group;
    }

  private:
    //np::ndarray
    np::ndarray run(int frame, string rgb_mode)
    {
      cout << "フレーム[処理開始] " << frame << endl;

      namespace OP = ObjectProgress;
      OP::ObjectProduction *object_production = new OP::ObjectProduction(frame, object_group, layer_layer_id, py_out_func, python_operation, video_image_control, editor, rgb_mode);
      object_production->production_order_decision();
      np::ndarray object_draw_base = object_production->production_object_group();
      //audio_function_list = object_production->get_audio_function_list();
      delete object_production;

      //object_draw_base[0:720,0:1280,0] *= object_draw_base[:][:][3];
      //object_draw_base[0:720,0:1280,1] *= object_draw_base[:][:][3];
      //object_draw_base[0:720,0:1280,2] *= object_draw_base[:][:][3];

      cout << "フレーム[処理終了] " << frame << endl;
      cout << " " << endl;

      return object_draw_base;
    }
  };
}

BOOST_PYTHON_MODULE(video_main)
{
  Py_Initialize();
  np::initialize();
  py::class_<VideoMain::VideoExecutionCenter>("VideoExecutionCenter",
                                              py::init<py::dict, py::dict>()) // VideoExecutionCenterコンストラクタへの引数型

      //.def("sta", &VideoExecutionCenter::sta)
      .def("scene_setup", &VideoMain::VideoExecutionCenter::scene_setup)
      .def("execution_main", &VideoMain::VideoExecutionCenter::execution_main)
      .def("execution_preview", &VideoMain::VideoExecutionCenter::execution_preview)
      .def("object_group_recovery", &VideoMain::VideoExecutionCenter::object_group_recovery);
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

// エフェクトを入れない方が重たくなる→値私だからでは