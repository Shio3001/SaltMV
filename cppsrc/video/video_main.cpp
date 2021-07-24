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
    py::dict effect_point_internal_id_time;
    vector<string> around_point_key;
    int now_frame;
    int before_time;
    int next_time;
    EffectProduction(int send_now_frame, py::dict &send_effect_group, py::dict &send_py_out_func, py::dict &send_python_operation, py::object &send_video_image_control, py::dict &send_editor, vector<string> send_around_point_key, py::dict &send_effect_point_internal_id_time)
    {
      effect_group = send_effect_group;
      py_out_func = send_py_out_func;
      python_operation = send_python_operation;
      video_image_control = send_video_image_control;
      around_point_key = send_around_point_key;
      editor = send_editor;
      now_frame = send_now_frame;
      effect_point_internal_id_time = send_effect_point_internal_id_time;

      cout << "EffectProduction"
           << " "
           << "before_time"
           << " "
           << "next_time"
           << " "
           << around_point_key[0]
           << " "
           << around_point_key[1] << endl;

      cout << "lord before_time" << endl;
      before_time = py::extract<int>(effect_point_internal_id_time[around_point_key[0]]);

      cout << "lord next_time" << endl;
      next_time = py::extract<int>(effect_point_internal_id_time[around_point_key[1]]);

      cout << before_time << " " << next_time << endl;
    }
    py::list production_effect_group()
    {
      cout << "production_effect_group" << endl;
      int effect_len = py::len(effect_group);
      py::tuple shape_size = py::make_tuple(editor["y"], editor["x"], 4);
      np::ndarray effect_draw_base = np::zeros(shape_size, np::dtype::get_builtin<uint>());

      cout << "effect_len"
           << " " << effect_len << endl;

      py::list effect_group_val = py::extract<py::list>(effect_group.values());

      py::list starting_point_center;

      for (int a = 0; a < 2; a++)
      {
        starting_point_center.append(0);
      }

      for (int i = 0; i < effect_len; i++)
      {
        py::tuple procedure_return = py::extract<py::tuple>(production_effect_individual(effect_draw_base, effect_group_val[i]));

        // ここから
        cout << "effect_draw_base" << endl;
        effect_draw_base = py::extract<np::ndarray>(procedure_return[0]);

        cout << "starting_point" << endl;
        py::list procedure_return_starting_point_center = py::extract<py::list>(procedure_return[1]);

        for (int a = 0; a < 2; a++)
        {
          cout << a << " procedure_return_starting_point_center " << endl;
          int spc = py::extract<int>(procedure_return_starting_point_center[a]);
          starting_point_center[a] += spc;
        }

        //starting_point_center[a] = starting_point_center[a] + py::extract<int>(procedure_return_starting_point_center[1]);
        //effect_draw_base = new_effect_draw_base;
      }
      cout << " effect_group_return A" << endl;

      py::list effect_group_return;

      cout << " effect_group_return a1" << endl;

      effect_group_return.append(effect_draw_base);

      cout << " effect_group_return a2" << endl;

      effect_group_return.append(starting_point_center);

      cout << " effect_group_return B" << endl;

      return effect_group_return;
    }
    py::tuple production_effect_individual(np::ndarray effect_draw_base, py::object effect)
    {
      cout << "production_effect_individual" << endl;

      py::dict effect_point_internal_id_point = py::extract<py::dict>(effect.attr("effect_point_internal_id_point"));
      string effect_name = py::extract<string>(effect.attr("effect_name"));
      string effect_id = py::extract<string>(effect.attr("effect_id"));
      py::dict various_fixed = py::extract<py::dict>(effect.attr("various_fixed"));
      //py::dict effect_point = py::extract<py::dict>(effect.attr("effect_point"));
      py::object procedure = py::extract<py::object>(effect.attr("procedure"));

      cout << "before_value"
           << " "
           << "next_value" << endl;

      py::dict before_value = py::extract<py::dict>(effect_point_internal_id_point[around_point_key[0]]);
      py::dict next_value = py::extract<py::dict>(effect_point_internal_id_point[around_point_key[1]]);

      py::list before_value_key = py::extract<py::list>(before_value.keys());
      py::list next_value_key = py::extract<py::list>(next_value.keys());

      py::list before_value_values = py::extract<py::list>(before_value.values());
      py::list next_value_values = py::extract<py::list>(next_value.values());

      cout << "before_value"
           << " "
           << "next_value"
           << " "
           << "end" << endl;

      if (before_time == next_time)
      {
        next_time += 1;
      }

      py::dict effect_value = {};

      int effect_point_len = py::len(effect_point_internal_id_point);
      int before_value_key_len = py::len(before_value_key);
      //int various_fixed_len = py::len(various_fixed);

      int b_n_time = next_time - before_time;
      int b_now_time = now_frame - before_time;

      cout << "before_value_key_len" << before_value_key_len << endl;

      for (int i = 0; i < before_value_key_len; i++)
      {
        cout << i << " "
             << "before_value_key_len" << endl;
        int pos = (py::extract<int>(next_value_values[i]) - py::extract<int>(before_value_values[i])) / b_n_time * b_now_time;
        effect_value[before_value_key[i]] = pos;
        cout << "pos : " << pos << endl;
      }

      cout << "effect_plugin_elements" << endl;
      py::object effect_plugin_elements = py::extract<py::object>(py_out_func["EffectPluginElements"](effect_draw_base, effect_value, before_value, next_value, now_frame, editor, python_operation));

      cout << "procedure_return" << endl;
      py::tuple procedure_return = py::extract<py::tuple>(procedure.attr("main")(effect_plugin_elements));

      //int starting_point_left_up[2];

      //starting_point_left_up[1] = py::extract<int>(starting_point_center[1]) - py::extract<int>(new_effect_draw_size[1]) / 2 + py::extract<int>(xy[1]) / 2;

      //ここまで座標中心が上地点

      cout << " "
           << "new_effect_draw_base end" << endl;

      return procedure_return;
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

        bool low = py::extract<int>(installation[0]) <= frame;
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
        else
        {
          cout << "(´･ω･`)" << endl;
        }
      }
      sort(order_decision_object_group_number.begin(), order_decision_object_group_number.end()); // vector
    }

    np::ndarray production_object_group()
    {

      py::tuple shape_size = py::make_tuple(editor["y"], editor["x"], 4);
      np::ndarray object_draw_base = np::zeros(shape_size, np::dtype::get_builtin<uint>());

      for (int i = 0; i < order_decision_object_group_number.size(); i++)
      {

        cout << i << " "
             << "production_object_group" << endl;
        int now_object_nun = order_decision_object_group_number[i];
        py::object now_objcet = order_decision_object_group[now_object_nun];

        np::ndarray new_object_draw_base = production_object_individual(now_objcet, object_draw_base);
        object_draw_base = new_object_draw_base;
      }

      return object_draw_base;
    }

    np::ndarray production_object_individual(py::object &now_objcet, np::ndarray object_individual_draw_base)
    {
      cout << "production_object_individual" << endl;

      py::dict effect_point_internal_id_time = py::extract<py::dict>(now_objcet.attr("effect_point_internal_id_time"));
      py::list id_time_key = py::extract<py::list>(effect_point_internal_id_time.keys());
      py::list id_time_value = py::extract<py::list>(effect_point_internal_id_time.values());
      vector<string> around_point_key = around_point_search(frame, id_time_key, id_time_value);
      py::dict effect_group = py::extract<py::dict>(now_objcet.attr("effect_group")); //ここ  now_objcet  に effect_pointがあるわけないやろばか
      string synthetic_type = py::extract<string>(now_objcet.attr("synthetic"));
      EP::EffectProduction *effect_production = new EP::EffectProduction(frame, effect_group, py_out_func, python_operation, video_image_control, editor, around_point_key, effect_point_internal_id_time);
      py::list effect_group_return = effect_production->production_effect_group();

      // ここから
      cout << "effect_group_return" << endl;
      np::ndarray new_effect_draw = py::extract<np::ndarray>(effect_group_return[0]);

      cout << "starting_point" << endl;
      py::list starting_point_center = py::extract<py::list>(effect_group_return[1]);

      //cout << starting_point_center[0] << " " << starting_point_center[1] << endl;

      py::tuple new_draw_size_shape = py::extract<py::tuple>(new_effect_draw.attr("shape"));

      int new_effect_draw_size[2];
      new_effect_draw_size[0] = py::extract<int>(new_draw_size_shape[1]);
      new_effect_draw_size[1] = py::extract<int>(new_draw_size_shape[0]);

      string xy[] = {"x",
                     "y"};

      py::list base_draw_range_lu;
      py::list base_draw_range_rd;

      py::list add_draw_range_lu;
      py::list add_draw_range_rd;

      for (int i = 0; i < 2; i++)
      {
        base_draw_range_lu.append(0);
        base_draw_range_rd.append(0);
        add_draw_range_lu.append(0);
        add_draw_range_rd.append(0);
        int draw_size = py::extract<int>(editor[xy[i]]);
        int new_draw_size = new_effect_draw_size[i];
        int center = py::extract<int>(starting_point_center[i]);

        int position_lu = center - new_draw_size / 2 + draw_size / 2; //重ね合わせたい左側座標
        int position_rd = position_lu + new_draw_size;                //重ね合わせたい右側座標

        if (position_lu < 0)
        {
          add_draw_range_lu[i] = abs(position_lu);
          base_draw_range_rd[i] = 0;
        }
        else
        {
          add_draw_range_lu[i] = 0;
          base_draw_range_lu[i] = position_lu;
        }

        if (position_rd > draw_size)
        {
          add_draw_range_rd[i] = draw_size - position_lu;
          base_draw_range_rd[i] = draw_size;
        }
        else
        {
          add_draw_range_rd[i] = new_draw_size;
          base_draw_range_rd[i] = position_rd;
        }

        //cout << i << " position_lu " << position_lu << " position_rd " << position_rd << " : base " << base_draw_range_rd[i] << " add " << add_draw_range_rd[i] << endl;
      }

      py::object synthetic_func = py::extract<py::object>(python_operation["synthetic"].attr("call"));
      np::ndarray sy_draw = py::extract<np::ndarray>(synthetic_func(synthetic_type, object_individual_draw_base, new_effect_draw, base_draw_range_lu, base_draw_range_rd, add_draw_range_lu, add_draw_range_rd));

      //np::ndarray new_object_individual_draw_base = py::extract<np::ndarray>(synthetic_func(synthetic_type, object_individual_draw_base, effect_draw));
      /*
      int xa = add_draw_range_lu[0];
      int xb = base_draw_range_lu[0];

      for (int x = 0; x < add_draw_range_rd[0] - add_draw_range_lu[0]; x++)
      {
        int ya = add_draw_range_lu[1];
        int yb = base_draw_range_lu[1];

        for (int y = 0; y < add_draw_range_rd[1] - add_draw_range_lu[1]; y++)
        {
          //py::tuple xbyb = py::make_tuple(xb, yb);
          //py::tuple xaya = py::make_tuple(xa, ya);
          //cout << "synthetic_func" << endl;
          //cout << " " << xb << " " << yb << " " << xa << " " << xb << endl;

          //cout << "A" << endl;

          //cout << -1 * xa << -1 * ya << -1 * xb << -1 * yb << endl;

          np::ndarray base_p = py::extract<np::ndarray>(object_individual_draw_base[yb][xb]);
          np::ndarray add_p = py::extract<np::ndarray>(new_effect_draw[ya][xa]);
          np::ndarray sy_draw = py::extract<np::ndarray>(synthetic_func(synthetic_type, base_p, add_p));
          //object_individual_draw_base[yb][xb] = sy_draw;
          //object_individual_draw_base[yb][xb]

          //cout << "E" << endl;

          ya++;
          yb++;
        }

        xa++;
        xb++;
      }

      */

      cout << "end" << endl;

      //np::ndarray base_range_draw = py::extract<np::ndarray>(object_individual_draw_base [base_draw_range_lu[0]:base_draw_range_rd[0], base_draw_range_lu[1]:base_draw_range_rd[1]]);
      //np::ndarray add_range_draw = py::extract<np::ndarray>(new_effect_draw [add_draw_range_lu[0]:add_draw_range_rd[0], add_draw_range_lu[1]:add_draw_range_rd[1]]);

      //delete synthetic_production;
      return object_individual_draw_base;
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
        if (target >= low_frame && target <= frame) //ここの条件式を直さないといけない
        {
          around_point[0] = py::extract<string>(id_time_key[i]);
          low_frame = py::extract<int>(id_time_value[i]);

          cout << "around_point[0] " << around_point[0] << endl;
        }
      }

      bool frag_high = false;
      int high_frame = 0;
      for (int i = 0; i < id_time_len; i++) //大きいあたい
      {
        int target = py::extract<int>(id_time_value[i]);
        if (target > high_frame && target > frame)
        {
          around_point[1] = py::extract<string>(id_time_key[i]);
          high_frame = py::extract<int>(id_time_value[i]);
          cout << "around_point[1] " << around_point[1] << endl;
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
      np::ndarray draw_all = np::zeros(shape_size, np::dtype::get_builtin<uint>());

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