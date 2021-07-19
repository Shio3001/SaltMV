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
    py::dict editor;
    vector<string> around_point_key;
    EffectProduction(py::dict &send_effect_group, py::dict &send_py_out_func, py::dict &send_python_operation, py::object &send_video_image_control, py::dict &send_editor, vector<string> send_around_point_key)
    {
      effect_group = send_effect_group;
      py_out_func = send_py_out_func;
      python_operation = send_python_operation;
      video_image_control = send_video_image_control;
      around_point_key = send_around_point_key;
      editor = send_editor;
    }
    np::ndarray production_effect_group()
    {
      int effect_len = py::len(effect_group);
      py::tuple shape_size = py::make_tuple(editor["y"], editor["x"], 4);
      np::ndarray effect_draw_base = np::zeros(shape_size, np::dtype::get_builtin<double>());

      for (int i = 0; i < effect_len; i++)
      {
        np::ndarray new_effect_draw_base = production_effect_individual(effect_draw_base, effect_group[i]);
        effect_draw_base = new_effect_draw_base;
      }

      return effect_draw_base;
    }
    np::ndarray production_effect_individual(np::ndarray effect_draw_base, py::object effect)
    {
      py::dict effect_point_internal_id_point = py::extract<py::dict>(effect.attr("effect_point_internal_id_point"));
      string effect_name = py::extract<string>(effect.attr("effect_name"));
      string effect_id = py::extract<string>(effect.attr("effect_id"));
      py::dict various_fixed = py::extract<py::dict>(effect.attr("various_fixed"));
      py::dict effect_point = py::extract<py::dict>(effect.attr("effect_point"));
      py::object procedure = py::extract<py::object>(effect.attr("procedure"));
      np::ndarray new_effect_draw_base = effect_draw_base;
      return new_effect_draw_base;
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
    py::dict editor;

    int object_len;

    ObjectProduction(int send_frame, py::dict &send_object_group, py::dict &send_layer_layer_id, py::dict &send_py_out_func, py::dict &send_python_operation, py::object &send_video_image_control, py::dict &send_editor)
    {
      frame = send_frame;
      object_group = send_object_group;
      layer_layer_id = send_layer_layer_id;
      py_out_func = send_py_out_func;
      python_operation = send_python_operation;
      video_image_control = send_video_image_control;
      object_len = py::len(object_group);
      editor = send_editor;
    }

    void production_order_decision()
    {
      for (int i = 0; i < object_len; i++)
      {

        py::object this_object = py::list(object_group.values())[i];
        py::list installation = py::extract<py::list>(this_object[0].attr("installation"));

        bool low = py::extract<int>(installation[0]) < frame;
        bool high = frame < py::extract<int>(installation[1]);

        if (low && high)
        {
          string layer_id = py::extract<string>(this_object[1]);

          py::object layer_number_func = py_out_func["layer_number"];

          int now_layer_number = py::extract<int>(layer_number_func(layer_id));

          order_decision_object_group[now_layer_number] = this_object[0];

          order_decision_object_group_number.push_back(now_layer_number);

          cout << "frame" << frame << " / now_layer_number " << now_layer_number << " / installation " << py::extract<int>(installation[0]) << " " << py::extract<int>(installation[1]) << " " << endl;
        }
      }
      sort(order_decision_object_group_number.begin(), order_decision_object_group_number.end()); // vector
    }

    np::ndarray production_object_group()
    {

      py::tuple shape_size = py::make_tuple(editor["y"], editor["x"], 4);
      np::ndarray object_draw_base = np::zeros(shape_size, np::dtype::get_builtin<double>());

      for (int i = 0; i < order_decision_object_group_number.size(); i++)
      {
        int now_object_nun = order_decision_object_group_number[i];
        py::object now_objcet = order_decision_object_group[now_object_nun];

        np::ndarray new_object_draw_base = production_object_individual(now_objcet, object_draw_base);
        object_draw_base = new_object_draw_base;
      }

      return object_draw_base;
    }

    np::ndarray production_object_individual(py::object &now_objcet, np::ndarray object_individual_draw_base)
    {
      py::dict effect_point_internal_id_time = py::extract<py::dict>(now_objcet.attr("effect_point_internal_id_time"));
      py::list id_time_key = py::extract<py::list>(effect_point_internal_id_time.keys());
      py::list id_time_value = py::extract<py::list>(effect_point_internal_id_time.values());
      vector<string> around_point_key = around_point_search(frame, id_time_key, id_time_value);
      py::dict effect_group = py::extract<py::dict>(now_objcet.attr("effect_point")); //ここ  now_objcet  に effect_pointがあるわけないやろばか
      string synthetic_type = py::extract<string>(now_objcet.attr("synthetic"));
      EP::EffectProduction *effect_production = new EP::EffectProduction(effect_group, py_out_func, python_operation, video_image_control, editor, around_point_key);
      np::ndarray effect_draw = effect_production->production_effect_group();

      py::object synthetic_func = py::extract<py::object>(python_operation["synthetic"].attr("call"));
      np::ndarray new_object_individual_draw_base = py::extract<np::ndarray>(synthetic_func(synthetic_type, object_individual_draw_base, effect_draw));
      delete effect_production;
      return new_object_individual_draw_base;
    }

    vector<string> around_point_search(int frame, py::list &id_time_key, py::list &id_time_value)
    {
      vector<string> around_point{"", ""};

      int id_time_len = py::len(id_time_key);
      bool frag_low = false;
      int low_frame = 0;
      for (int i = 0; i < id_time_len; i++) //低い値
      {
        int target = py::extract<int>(id_time_value[i]);
        if (low_frame < target && target < frame)
        {
          around_point[0] = py::extract<string>(id_time_key[i]);
          low_frame = py::extract<int>(id_time_value[i]);
        }
      }

      bool frag_high = false;
      int high_frame = 0;
      for (int i = 0; i < id_time_len; i++) //大きいあたい
      {
        int target = py::extract<int>(id_time_value[i]);
        if (high_frame > target && target > frame)
        {
          around_point[1] = py::extract<string>(id_time_key[i]);
          high_frame = py::extract<int>(id_time_value[i]);
        }
      }
      return around_point;
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

    np::ndarray execution_main(int sta = -1, int end = -1)
    {
      //vector<np::ndarray> draw_vector;

      if (sta == -1)
      {
        sta = 0;
      }
      if (end == -1)
      {
        end = py::extract<int>(editor["len"]);
      }
      py::tuple shape_size = py::make_tuple(end - sta, editor["y"], editor["x"], 4);
      np::ndarray draw_all = np::zeros(shape_size, np::dtype::get_builtin<double>());

      for (int i = sta; i < end; i++)
      {
        np::ndarray draw = run(i);
        //cout << py::extract<int>(draw.attr("shape")[0]) << " " << i << endl;
        //draw_all.push_back(draw);
        draw_all[i - sta] = draw;
      }

      return draw_all;
    }

    np::ndarray execution_preview(int frame)
    {
      if (frame > py::extract<int>(editor["len"]))
      {
        frame = py::extract<int>(editor["len"]);
      }

      np::ndarray draw = run(frame);
      return draw;
    }

  private:
    //np::ndarray
    np::ndarray run(int frame)
    {
      namespace OP = ObjectProgress;
      OP::ObjectProduction *object_production = new OP::ObjectProduction(frame, object_group, layer_layer_id, py_out_func, python_operation, video_image_control, editor);

      object_production->production_order_decision();
      np::ndarray object_draw_base = object_production->production_object_group();

      delete object_production;

      return object_draw_base;
    }
  };
}

BOOST_PYTHON_MODULE(video_main)
{
  Py_Initialize();
  np::initialize();
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