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

#include "../plugin/synthetic/normal.hpp"
SyntheticNormal synthetic_normal;

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
      //cout << "production_order_decision" << endl;

      for (int i = 0; i < object_len; i++)
      {
        cout << "object_len loop " << i << endl;

        py::object object_group_values = object_group.attr("values")();

        //cout << "object_group_values" << endl;

        py::object this_object = py::list(object_group_values)[i];

        //cout << "this_object" << endl;

        py::list installation = py::extract<py::list>(this_object[0].attr("installation"));

        //cout << "installation" << endl;

        int installation_sta = py::extract<double>(installation[0]);
        int installation_end = py::extract<double>(installation[1]);

        //cout << "installation_int" << endl;

        bool low = installation_sta <= frame;
        bool high = frame < installation_end;

        //cout << "low high " << low << high << endl;

        if (low && high)
        {
          string layer_id = py::extract<string>(this_object[1]);

          py::object layer_number_func = py_out_func["layer_number"];

          int now_layer_number = py::extract<double>(layer_number_func(layer_id));

          order_decision_object_group[now_layer_number] = this_object[0];

          order_decision_object_group_number.push_back(now_layer_number);

          //cout << "frame" << frame << " / now_layer_number " << now_layer_number << " / installation " << py::extract<double>(installation[0]) << " " << py::extract<double>(installation[1]) << " " << endl;
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

      int editor_x = py::extract<double>(editor["x"]);
      int editor_y = py::extract<double>(editor["y"]);

      int *draw = new int[editor_y * editor_x * 3];
      int now_xy_size[2] = {editor_x, editor_y};

      for (int i = 0; i < order_decision_object_group_number.size(); i++)
      {

        cout << i << " "
             << "production_object_group" << endl;
        int now_object_nun = order_decision_object_group_number[i];
        py::object now_objcet = order_decision_object_group[now_object_nun];

        production_object_individual(now_objcet, draw, now_xy_size);
      }

      cout << "cpp -> numpy" << endl;

      //py::tuple shape = py::make_tuple(editor_y, editor_x, 3);
      py::tuple shape = py::make_tuple(editor_y * editor_x * 3);
      py::tuple stride = py::make_tuple(sizeof(int));
      np::dtype dt = np::dtype::get_builtin<uint>();
      np::ndarray object_draw_base = np::from_data(&draw[0], dt, shape, stride, py::object());
      //np::ndarray object_draw_base = np::from_data(&draw[0], dt, shape, stride, py::object());
      //  np::ndarray output = np::from_data(&v[0], dt, shape, stride, py::object());

      cout << "cpp -> numpy end" << endl;

      return object_draw_base;
    }

    int production_object_individual(py::object &now_objcet, int *draw_object_draw_base, int *now_xy_size)
    {
      //cout << "production_object_individual" << endl;

      py::dict effect_point_internal_id_time = py::extract<py::dict>(now_objcet.attr("effect_point_internal_id_time"));
      py::list id_time_key = py::extract<py::list>(effect_point_internal_id_time.keys());
      py::list id_time_value = py::extract<py::list>(effect_point_internal_id_time.values());

      py::list installation = py::extract<py::list>(now_objcet.attr("installation"));

      int installation_sta = py::extract<double>(installation[0]);
      int installation_end = py::extract<double>(installation[1]);

      vector<string> around_point_key = around_point_search(frame, id_time_key, id_time_value, installation_sta, installation_end);
      py::object effect_group = now_objcet.attr("effect_group"); //ここ  now_objcet  に effect_pointがあるわけないやろばか
      string synthetic_type = py::extract<string>(now_objcet.attr("synthetic"));
      EP::EffectProduction *effect_production = new EP::EffectProduction(frame, effect_group, py_out_func, python_operation, video_image_control, editor, around_point_key, effect_point_internal_id_time, installation_sta, installation_end);
      py::list effect_group_return = effect_production->production_effect_group();

      // ここから
      //cout << "effect_group_return" << endl;
      np::ndarray new_effect_draw = py::extract<np::ndarray>(effect_group_return[0]);
      py::list starting_point_center = py::extract<py::list>(effect_group_return[1]);

      //py::list new_audio_function_list = py::extract<py::list>(effect_group_return[2]);

      //audio_function_list.extend(new_audio_function_list);

      ////cout << starting_point_center[0] << " " << starting_point_center[1] << endl;

      py::tuple new_draw_size_shape = py::extract<py::tuple>(new_effect_draw.attr("shape"));
      int new_effect_draw_size[3];
      new_effect_draw_size[0] = py::extract<double>(new_draw_size_shape[1]);
      new_effect_draw_size[1] = py::extract<double>(new_draw_size_shape[0]);
      new_effect_draw_size[2] = py::extract<double>(new_draw_size_shape[2]);

      int effect_draw_size_multiplication = new_effect_draw_size[0] * new_effect_draw_size[1] * new_effect_draw_size[2];

      cout << "new_effect_draw_size " << new_effect_draw_size[0] << " " << new_effect_draw_size[1] << " " << new_effect_draw_size[2] << endl;

      string xy[] = {"x",
                     "y"};

      vector<int> base_draw_range_lu = {0, 0};
      vector<int> base_draw_range_rd = {0, 0};
      vector<int> add_draw_range_lu = {0, 0};
      vector<int> add_draw_range_rd = {0, 0};

      for (int i = 0; i < 2; i++)
      {

        int draw_size = now_xy_size[i];
        int new_draw_size = new_effect_draw_size[i];
        int center = py::extract<double>(starting_point_center[i]);

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

        //cout << i << " position_lu " << position_lu << " position_rd " << position_rd << endl;
        //cout << "add_draw_range_lu " << add_draw_range_lu[i] << " base_draw_range_lu " << base_draw_range_lu[i] << endl;
        //cout << "add_draw_range_rd " << add_draw_range_rd[i] << " base_draw_range_rd " << base_draw_range_rd[i] << endl;

        ////cout << i << " position_lu " << position_lu << " position_rd " << position_rd << " : base " << base_draw_range_rd[i] << " add " << add_draw_range_rd[i] << endl;
      }

      cout << "synthetic_func" << endl;
      cout << "effect_draw_size_multiplication " << effect_draw_size_multiplication << endl;

      bool cpptype = python_operation["plugin"]["synthetic"][synthetic_type] == "TypeHppfileDefaultInclude";
      // new_effect_draw.attr("reshape")(effect_draw_size_multiplication);

      // int shape_new = py::extract<int>(new_effect_draw.attr("shape")[0]);
      // cout << shape_new << endl;
      // int shape_new2 = py::extract<int>(new_effect_draw.attr("shape")[1]);
      // cout << shape_new2 << endl;
      // int shape_new3 = py::extract<int>(new_effect_draw.attr("shape")[2]);
      // cout << shape_new3 << endl;

      auto *start_pointer_numpy = reinterpret_cast<int *>(new_effect_draw.get_data());

      //py::tuple new_shape = py::make_tuple(new_effect_draw_size[0] * new_effect_draw_size[1] * new_effect_draw_size[2]);
      //np::ndarray new_effect_draw_one_dimension = np::reshape(new_effect_draw,(-1));
      //auto *start_pointer_numpy = reinterpret_cast<int *>(new_effect_draw.get_data());
      cout << "cpptype" << cpptype << endl;

      int test = 0;

      if (cpptype)
      {
        int ya = add_draw_range_lu[1];
        for (int yb = base_draw_range_lu[1]; yb < base_draw_range_rd[1]; yb++)
        {
          int xa = add_draw_range_lu[0];
          for (int xb = base_draw_range_lu[0]; xb < base_draw_range_rd[0]; xb++)
          {
            //cout << "setup" << endl;

            int ipxA = (now_xy_size[0] * ya + xa) * 4;
            int ipxB = (now_xy_size[0] * yb + xb) * 3;

            int calculation[4];
            int source[4];
            int additions[4];

            //cout << "source" << endl;

            //cout << " py -> cpp" << endl;

            for (int i = 0; i < 3; i++)
            {
              source[i] = draw_object_draw_base[ipxB + i];
            }
            source[3] = 255;

            for (int i = 0; i < new_effect_draw_size[2]; i++)
            {
              //3686400
              //cout << test << " " << ya << " " << xa << " " << new_effect_draw_size[0] * new_effect_draw_size[1] * new_effect_draw_size[2] << endl;
              //cout << "additions" << ya << " " << xa << " " << i << " " << test << endl;

              //additions[i]  = new_effect_draw[ya][xa][i];

              additions[i] = *start_pointer_numpy;

              // cout << "A" << endl;
              // auto now_pointer_numpy = start_pointer_numpy + (now_xy_size[0] * ya + xa) * new_effect_draw_size[2] + i;
              // cout << "B" << endl;
              // additions[i] = *now_pointer_numpy;
              // cout << "C" << endl;
              // cout << test << endl;
              // test++;

              start_pointer_numpy++;
              //cout << xa << " " << ya << endl;
            }

            //cout << "synthetic_normal" << endl;

            //cout << " A -> cpp" << endl;

            if (synthetic_type == "normal")
            {
              synthetic_normal.run(calculation, source, additions);
            }

            //cout << "read" << endl;
            double A = calculation[3];
            int R = calculation[0] * (A / 255.0); //透明度反映
            int G = calculation[1] * (A / 255.0);
            int B = calculation[2] * (A / 255.0);

            //cout << "RGB" << endl;

            draw_object_draw_base[ipxB + 0] = R;
            draw_object_draw_base[ipxB + 1] = G;
            draw_object_draw_base[ipxB + 2] = B;

            xa++;

            //cout << "end" << endl;
          }
          ya++;
        }
      }
      else
      {
      }

      //py::object synthetic_func = py::extract<py::object>(python_operation["synthetic"].attr("call"));
      //np::ndarray sy_draw = py::extract<np::ndarray>(synthetic_func(synthetic_type, object_individual_draw_base, new_effect_draw, list_base_draw_range_lu, list_base_draw_range_rd, list_add_draw_range_lu, list_add_draw_range_rd));

      cout << "synthetic_func2" << endl;

      //return sy_draw;
    }

    vector<string> around_point_search(int frame, py::list &id_time_key, py::list &id_time_value, int installation_sta, int installation_end)
    {
      vector<string> around_point{"", ""};

      int id_time_len = py::len(id_time_key);
      bool frag_low = false;
      int low_frame = 0;
      for (int i = 0; i < id_time_len; i++) //低い値
      {
        int target = py::extract<double>(id_time_value[i]);
        if (target >= low_frame && target <= frame) //ここの条件式を直さないといけない
        {
          around_point[0] = py::extract<string>(id_time_key[i]);
          low_frame = py::extract<double>(id_time_value[i]);

          //cout << "around_point[0] " << around_point[0] << endl;
        }
      }

      bool frag_high = false;
      int high_frame = py::extract<double>(editor["len"]);
      for (int i = 0; i < id_time_len; i++) //大きいあたい
      {
        int target = py::extract<double>(id_time_value[i]);
        if (target <= high_frame && target > frame)
        {
          around_point[1] = py::extract<string>(id_time_key[i]);
          high_frame = py::extract<double>(id_time_value[i]);
          //cout << "around_point[1] " << around_point[1] << endl;
        }
        else if (frame == installation_end)
        {
          around_point[1] = "default_end";
          high_frame = py::extract<double>(id_time_value[i]);
          //cout << "around_point[1] " << around_point[1] << endl;
        }
      }

      return around_point;
    }
  };
}