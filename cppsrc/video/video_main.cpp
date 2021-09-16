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

namespace EffectProgress
{
  class EffectProduction
  {
  public:
    py::object effect_group;
    py::dict py_out_func;
    py::dict python_operation;
    py::object video_image_control;
    py::dict editor;
    py::dict effect_point_internal_id_time;
    vector<string> around_point_key;
    int now_frame;
    int before_time;
    int next_time;
    int installation_sta;
    int installation_end;

    //py::list audio_object;

    EffectProduction(int send_now_frame, py::object &send_effect_group, py::dict &send_py_out_func, py::dict &send_python_operation, py::object &send_video_image_control, py::dict &send_editor, vector<string> send_around_point_key, py::dict &send_effect_point_internal_id_time, int send_installation_sta, int send_installation_end)
    {
      effect_group = send_effect_group;
      py_out_func = send_py_out_func;
      python_operation = send_python_operation;
      video_image_control = send_video_image_control;
      around_point_key = send_around_point_key;
      editor = send_editor;
      now_frame = send_now_frame;
      effect_point_internal_id_time = send_effect_point_internal_id_time;

      installation_sta = send_installation_sta;
      installation_end = send_installation_end;

      //cout << "EffectProduction"
      /*
      << " "
      << "before_time"
      << " "
      << "next_time"
      << " "
      << around_point_key[0]
      << " "
      << around_point_key[1] << endl;*/

      //cout << "lord before_time" << endl;
      before_time = py::extract<int>(effect_point_internal_id_time[around_point_key[0]]);

      //cout << "lord next_time" << endl;
      next_time = py::extract<int>(effect_point_internal_id_time[around_point_key[1]]);

      cout << before_time << " " << next_time << endl;

      //cout << before_time << " " << next_time << endl;
    }
    /*py::list get_audio_object()
    {
      return audio_object;
    }*/

    py::list production_effect_group()
    {
      //cout << "production_effect_group" << endl;
      int effect_len = py::len(effect_group);
      py::tuple shape_size = py::make_tuple(editor["y"], editor["x"], 4);
      np::ndarray effect_draw_base = np::zeros(shape_size, np::dtype::get_builtin<uint>());

      //cout << "effect_len"
      //<< " " << effect_len << endl;

      py::object effect_group_val = py::list(effect_group.attr("values")());

      py::list starting_point_center;

      for (int a = 0; a < 2; a++)
      {
        starting_point_center.append(0);
      }

      for (int i = 0; i < effect_len; i++)
      {
        cout << "effect_group_val" << endl;

        py::object send_effect = effect_group_val[i];

        cout << "send_effect" << endl;

        py::tuple procedure_return = py::extract<py::tuple>(production_effect_individual(effect_draw_base, send_effect));

        // ここから
        cout << "effect_draw_base" << endl;
        effect_draw_base = py::extract<np::ndarray>(procedure_return[0]);

        cout << "starting_point" << endl;
        py::list procedure_return_starting_point_center = py::extract<py::list>(procedure_return[1]);

        for (int a = 0; a < 2; a++)
        {
          //cout << a << " procedure_return_starting_point_center " << endl;
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

      //effect_group_return.append(audio_object);

      cout << " effect_group_return B" << endl;

      return effect_group_return;
    }
    py::tuple production_effect_individual(np::ndarray &effect_draw_base, py::object &send_effect)
    {
      cout << "production_effect_individual" << endl;

      py::object effect = send_effect;

      py::dict effect_point_internal_id_point = py::extract<py::dict>(effect.attr("effect_point_internal_id_point"));
      string effect_name = py::extract<string>(effect.attr("effect_name"));
      string effect_id = py::extract<string>(effect.attr("effect_id"));
      py::dict various_fixed = py::extract<py::dict>(effect.attr("various_fixed"));
      //py::dict effect_point = py::extract<py::dict>(effect.attr("effect_point"));
      py::object procedure = effect.attr("procedure");
      bool audio = effect.attr("audio");

      //string test_txt1 = py::extract<string>(py::extract<py::object>(procedure.attr("now_file")));
      cout << "procedure " << endl;

      string cpp_file = py::extract<string>(effect.attr("cpp_file"));

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

      int b_n_section_time = next_time - before_time;
      int b_now_time = now_frame - before_time;

      cout << "before_value_key_len" << before_value_key_len << endl;

      for (int i = 0; i < before_value_key_len; i++)
      {
        //cout << i << " " << "before_value_key_len" << endl;
        int next = py::extract<int>(next_value_values[i]);
        int before = py::extract<int>(before_value_values[i]);
        double all_section = next - before;
        double one_section = all_section / b_n_section_time;
        double now_section = one_section * b_now_time;

        //ここら辺doubleじゃないと精密さが失われて中間点を経由する時に誤差が出る
        //なお被演算数値がどちらもint型だと出力もintになってしまうので注意
        int pos = now_section + before;
        effect_value[before_value_key[i]] = pos;

        string test_text = py::extract<string>(before_value_key[i]);

        cout << test_text << " " << pos << " " << one_section << " " << before << " " << next << " " << b_n_section_time << " " << b_now_time << endl;
        //cout << "pos : " << pos << endl;
      }

      //py::object FileSystem = py::extract<py::object>(py_out_func["FileSystem"]);

      //string effect_id =

      cout << "effect_plugin_elements" << endl;
      py::object effect_plugin_elements = py::extract<py::object>(py_out_func["EffectPluginElements"](effect_draw_base, effect_id, effect_value, before_value, next_value, various_fixed, now_frame, b_now_time, editor, python_operation, installation_sta, installation_end));

      cout << "procedure_return" << endl;
      py::object main_function = procedure.attr("main");

      cout << "procedure_return2" << endl;

      //py::object main_function_self = py::extract<py::object>(main_function.attr("__func__"));
      //py::object run_main_function = py::extract<py::object>(py_out_func["plugin_run"]);

      //py::object self_data = py::extract<py::object>(main_function.attr("__self__"));
      py::tuple procedure_return = py::extract<py::tuple>(main_function(effect_plugin_elements));

      /*
      if (audio == true)
      {
        py::list temp_audio_object_add;
        temp_audio_object_add.append(procedure.attr("sound"));
        temp_audio_object_add.append(procedure.attr("sound_init"));
        temp_audio_object_add.append(procedure.attr("sound_stop"));
        temp_audio_object_add.append(procedure.attr("get_now_file"));
        audio_object.append(temp_audio_object_add);
      }*/

      //string test_txt2 = py::extract<string>(py::extract<py::object>(procedure.attr("now_file")));
      //cout << "procedure2 " << test_txt2 << endl;

      cout << "effect終了" << endl;

      //int starting_point_left_up[2];

      //starting_point_left_up[1] = py::extract<int>(starting_point_center[1]) - py::extract<int>(new_effect_draw_size[1]) / 2 + py::extract<int>(xy[1]) / 2;

      //ここまで座標中心が上地点

      //cout << " "
      //<< "new_effect_draw_base end" << endl;

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
    py::object object_group;
    py::dict layer_layer_id;
    map<int, py::object> order_decision_object_group;
    vector<int> order_decision_object_group_number;
    py::dict editor;

    int object_len;

    ObjectProduction(int send_frame, py::object &send_object_group, py::dict &send_layer_layer_id, py::dict &send_py_out_func, py::dict &send_python_operation, py::object &send_video_image_control, py::dict &send_editor)
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
        py::object object_group_values = object_group.attr("values")();

        py::object this_object = py::list(object_group_values)[i];
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

          //cout << "frame" << frame << " / now_layer_number " << now_layer_number << " / installation " << py::extract<int>(installation[0]) << " " << py::extract<int>(installation[1]) << " " << endl;
        }
        else
        {
          //cout << "(´･ω･`)" << endl;
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

        //cout << i << " "
        //<< "production_object_group" << endl;
        int now_object_nun = order_decision_object_group_number[i];
        py::object now_objcet = order_decision_object_group[now_object_nun];

        np::ndarray new_object_draw_base = production_object_individual(now_objcet, object_draw_base);
        object_draw_base = new_object_draw_base;
      }

      return object_draw_base;
    }

    np::ndarray production_object_individual(py::object &now_objcet, np::ndarray &object_individual_draw_base)
    {
      //cout << "production_object_individual" << endl;

      py::dict effect_point_internal_id_time = py::extract<py::dict>(now_objcet.attr("effect_point_internal_id_time"));
      py::list id_time_key = py::extract<py::list>(effect_point_internal_id_time.keys());
      py::list id_time_value = py::extract<py::list>(effect_point_internal_id_time.values());

      py::list installation = py::extract<py::list>(now_objcet.attr("installation"));

      int installation_sta = py::extract<int>(installation[0]);
      int installation_end = py::extract<int>(installation[1]);

      vector<string> around_point_key = around_point_search(frame, id_time_key, id_time_value, installation_sta, installation_end);
      py::object effect_group = now_objcet.attr("effect_group"); //ここ  now_objcet  に effect_pointがあるわけないやろばか
      string synthetic_type = py::extract<string>(now_objcet.attr("synthetic"));
      EP::EffectProduction *effect_production = new EP::EffectProduction(frame, effect_group, py_out_func, python_operation, video_image_control, editor, around_point_key, effect_point_internal_id_time, installation_sta, installation_end);
      py::list effect_group_return = effect_production->production_effect_group();

      // ここから
      //cout << "effect_group_return" << endl;
      np::ndarray new_effect_draw = py::extract<np::ndarray>(effect_group_return[0]);

      //cout << "starting_point" << endl;
      py::list starting_point_center = py::extract<py::list>(effect_group_return[1]);

      //py::list new_audio_function_list = py::extract<py::list>(effect_group_return[2]);

      //audio_function_list.extend(new_audio_function_list);

      ////cout << starting_point_center[0] << " " << starting_point_center[1] << endl;

      py::tuple new_draw_size_shape = py::extract<py::tuple>(new_effect_draw.attr("shape"));

      int new_effect_draw_size[2];
      new_effect_draw_size[0] = py::extract<int>(new_draw_size_shape[1]);
      new_effect_draw_size[1] = py::extract<int>(new_draw_size_shape[0]);

      string xy[] = {"x",
                     "y"};

      py::list list_base_draw_range_lu;
      py::list list_base_draw_range_rd;
      py::list list_add_draw_range_lu;
      py::list list_add_draw_range_rd;

      vector<int> base_draw_range_lu = {0, 0};
      vector<int> base_draw_range_rd = {0, 0};
      vector<int> add_draw_range_lu = {0, 0};
      vector<int> add_draw_range_rd = {0, 0};

      for (int i = 0; i < 2; i++)
      {

        int draw_size = py::extract<int>(editor[xy[i]]);
        int new_draw_size = new_effect_draw_size[i];
        int center = py::extract<int>(starting_point_center[i]);

        //ここから基準点が左下に変わります

        int position_lu = center - (new_draw_size / 2) + (draw_size / 2); //重ね合わせたい左側座標
        int position_rd = position_lu + new_draw_size;                    //重ね合わせたい右側座標

        add_draw_range_lu[i] = 0;
        base_draw_range_lu[i] = position_lu;

        add_draw_range_rd[i] = new_draw_size;
        base_draw_range_rd[i] = position_rd;

        //そもそも範囲外

        if (position_rd < 0 || position_lu > draw_size)
        {
          add_draw_range_lu[i] = 0;
          base_draw_range_lu[i] = 0;
          add_draw_range_rd[i] = 0;
          base_draw_range_rd[i] = 0;
        }

        //左右ともにダメな時

        else if (position_lu < 0 && position_rd > draw_size)
        {
          cout << "左右ともにダメな時" << position_lu << " " << position_rd << " " << draw_size << endl;
          add_draw_range_lu[i] = abs(position_lu);
          add_draw_range_rd[i] = draw_size + abs(position_lu);

          base_draw_range_lu[i] = 0;
          base_draw_range_rd[i] = draw_size;
        }

        //左側だけダメ

        else if (position_lu < 0)
        {
          add_draw_range_lu[i] += abs(position_lu);
          base_draw_range_lu[i] = 0;
        }

        //右側だけダメ

        else if (position_rd > draw_size)
        {
          add_draw_range_rd[i] -= (position_rd - draw_size);
          base_draw_range_rd[i] = draw_size;
        }

        cout << i << " position_lu " << position_lu << " position_rd " << position_rd << endl;
        cout << "add_draw_range_lu " << add_draw_range_lu[i] << " base_draw_range_lu " << base_draw_range_lu[i] << endl;
        cout << "add_draw_range_rd " << add_draw_range_rd[i] << " base_draw_range_rd " << base_draw_range_rd[i] << endl;

        list_base_draw_range_lu.append(base_draw_range_lu[i]);
        list_base_draw_range_rd.append(base_draw_range_rd[i]);
        list_add_draw_range_lu.append(add_draw_range_lu[i]);
        list_add_draw_range_rd.append(add_draw_range_rd[i]);

        ////cout << i << " position_lu " << position_lu << " position_rd " << position_rd << " : base " << base_draw_range_rd[i] << " add " << add_draw_range_rd[i] << endl;
      }

      py::object synthetic_func = py::extract<py::object>(python_operation["synthetic"].attr("call"));
      np::ndarray sy_draw = py::extract<np::ndarray>(synthetic_func(synthetic_type, object_individual_draw_base, new_effect_draw, list_base_draw_range_lu, list_base_draw_range_rd, list_add_draw_range_lu, list_add_draw_range_rd));

      return sy_draw;
    }

    vector<string> around_point_search(int frame, py::list &id_time_key, py::list &id_time_value, int installation_sta, int installation_end)
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
      int high_frame = py::extract<int>(editor["len"]);
      for (int i = 0; i < id_time_len; i++) //大きいあたい
      {
        int target = py::extract<int>(id_time_value[i]);
        if (target <= high_frame && target > frame)
        {
          around_point[1] = py::extract<string>(id_time_key[i]);
          high_frame = py::extract<int>(id_time_value[i]);
          cout << "around_point[1] " << around_point[1] << endl;
        }
        else if (frame == installation_end)
        {
          around_point[1] = "default_end";
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

      int maxlen = py::extract<int>(editor["len"]);

      if (frame < 0)
      {
        frame = 0;
      }
      if (frame > maxlen)
      {
        frame = maxlen;
      }

      np::ndarray draw = run(frame);

      return draw;
    }

    np::ndarray execution_preview(int frame)
    {
      if (frame > py::extract<int>(editor["len"]))
      {
        frame = py::extract<int>(editor["len"]);
      }

      np::ndarray draw = run(frame);
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
    np::ndarray run(int frame)
    {
      cout << "フレーム[処理開始] " << frame << endl;

      namespace OP = ObjectProgress;
      OP::ObjectProduction *object_production = new OP::ObjectProduction(frame, object_group, layer_layer_id, py_out_func, python_operation, video_image_control, editor);
      object_production->production_order_decision();
      np::ndarray object_draw_base = object_production->production_object_group();
      //audio_function_list = object_production->get_audio_function_list();
      delete object_production;

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