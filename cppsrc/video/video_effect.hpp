
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
        py::object effect_group;
        py::dict py_out_func;
        py::dict python_operation;
        py::object video_image_control;
        py::dict editor;
        py::dict effect_point_internal_id_time;
        vector<string> around_point_key;
        map<string, float> *accompany_value;
        int now_frame;
        int before_time;
        int next_time;
        int installation_sta;
        int installation_end;

        //py::list audio_object;

        EffectProduction(int send_now_frame, py::object &send_effect_group, py::dict &send_py_out_func, py::dict &send_python_operation, py::object &send_video_image_control, py::dict &send_editor, vector<string> send_around_point_key, py::dict &send_effect_point_internal_id_time, int send_installation_sta, int send_installation_end, map<string, float> &send_accompany_value)
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

            before_time = py::extract<float>(effect_point_internal_id_time[around_point_key[0]]);
            next_time = py::extract<float>(effect_point_internal_id_time[around_point_key[1]]);

            accompany_value = &send_accompany_value;

            cout << before_time << " " << next_time << endl;
        }

        float BezierFunction(float t, float xy1, float xy2, float xy3, float xy4)
        {
            float tp = 1 - t;
            float bezier_result = pow(tp, 3) * xy1 +
                                  3 * pow(tp, 2) * t * xy2 +
                                  3 * tp * pow(t, 2) * xy3 +
                                  pow(t, 3) * xy4;
            return bezier_result;
        }

        py::list production_effect_group()
        {
            //cout << "production_effect_group" << endl;
            int effect_len = py::len(effect_group);
            py::tuple shape_size = py::make_tuple(editor["y"], editor["x"], 4);
            np::ndarray effect_draw_base = np::zeros(shape_size, np::dtype::get_builtin<uint>());
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

                string procedure_return_type = py::extract<string>(procedure_return[0]);

                if (procedure_return_type == "DRAW")
                {
                    effect_draw_base = py::extract<np::ndarray>(procedure_return[1]);
                    py::list procedure_return_starting_point_center = py::extract<py::list>(procedure_return[2]);
                    for (int a = 0; a < 2; a++)
                    {
                        int spc = py::extract<float>(procedure_return_starting_point_center[a]);
                        starting_point_center[a] += spc;
                    }
                }
                if (procedure_return_type == "ACCOMPANY")
                {

                    string key = py::extract<string>(procedure_return[1]);
                    float val = py::extract<float>(procedure_return[2]);
                    //accompany_value[key] = val;
                    //(*ss)[key]
                    (*accompany_value)[key] = val;
                }
                if (procedure_return_type == "AUDIO")
                {
                    //audioが来たとき
                }
            }
            cout << " effect_group_return A" << endl;
            py::list effect_group_return;
            cout << " effect_group_return a1" << endl;
            effect_group_return.append(effect_draw_base);
            cout << " effect_group_return a2" << endl;
            effect_group_return.append(starting_point_center);
            cout << " effect_group_return B" << endl;

            cout << "shapeテスト" << endl;

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
            py::dict accompany_target = py::extract<py::dict>(effect.attr("accompany_target"));

            py::dict easing_number = py::extract<py::dict>(effect.attr("easing_number"));

            //py::dict effect_point = py::extract<py::dict>(effect.attr("effect_point"));
            py::object procedure = effect.attr("procedure");

            //string test_txt1 = py::extract<string>(py::extract<py::object>(procedure.attr("now_file")));
            cout << "procedure " << endl;

            string cpp = py::extract<string>(effect.attr("cpp"));

            cout << "before_value"
                 << " "
                 << "next_value" << endl;

            py::dict first_value = py::extract<py::dict>(effect_point_internal_id_point["default_sta"]);

            py::dict before_value = py::extract<py::dict>(effect_point_internal_id_point[around_point_key[0]]);
            py::dict next_value = py::extract<py::dict>(effect_point_internal_id_point[around_point_key[1]]);

            py::list before_value_key = py::extract<py::list>(before_value.keys());
            py::list next_value_key = py::extract<py::list>(next_value.keys());

            py::list before_value_values = py::extract<py::list>(before_value.values());
            py::list next_value_values = py::extract<py::list>(next_value.values());

            py::list first_value_key = py::extract<py::list>(first_value.keys());
            py::list first_value_values = py::extract<py::list>(first_value.values());

            py::list accompany_target_values = py::extract<py::list>(accompany_target.values());

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

            float b_n_section_time = next_time - before_time;
            float b_now_time = now_frame - before_time;

            cout << "before_value_key_len" << before_value_key_len << endl;

            for (int i = 0; i < before_value_key_len; i++)
            {
                //cout << i << " " << "before_value_key_len" << endl;
                int next = py::extract<float>(next_value_values[i]);
                int before = py::extract<float>(before_value_values[i]);
                float all_section = next - before;
                // float one_section = all_section / b_n_section_time;
                // float now_section = one_section * b_now_time;

                float rate = b_now_time / b_n_section_time;

                py::object easing_data = easing_number[before_value_key[i]];
                float gx = py::extract<float>(easing_data.attr("gx"));
                float gy = py::extract<float>(easing_data.attr("gy"));
                float rx = py::extract<float>(easing_data.attr("rx"));
                float ry = py::extract<float>(easing_data.attr("ry"));
                cout << "gx gy rx ry";
                cout << gx;
                cout << " ";
                cout << gy;
                cout << " ";
                cout << rx;
                cout << " ";
                cout << ry;
                cout << " " << endl;

                float now_x_rate;
                now_x_rate = BezierFunction(rate, 0, gx, rx, 100) / 100;

                float now_y_rate;
                now_y_rate = BezierFunction(rate, 0, gy, ry / 100, 1);

                cout << "now_x_rate" << rate << " " << now_x_rate << endl;
                cout << "now_y_rate" << rate << " " << now_y_rate << endl;

                float now_section = all_section * now_y_rate;

                //ここら辺floatじゃないと精密さが失われて中間点を経由する時に誤差が出る
                //なお被演算数値がどちらもint型だと出力もintになってしまうので注意
                float pos = now_section + before;

                string accompany_key = py::extract<string>(accompany_target_values[i]);

                bool existence = accompany_value->find(accompany_key) != accompany_value->end();

                cout << "accompany_key" << existence << endl;

                if (existence)
                {
                    //(*accompany_value)[accompany_key] = val;
                    pos += (*accompany_value)[accompany_key];
                    cout << "accompany_key 加算" << (*accompany_value)[accompany_key] << endl;
                }

                effect_value[before_value_key[i]] = pos;

                string test_text = py::extract<string>(before_value_key[i]);

                //cout << test_text << " " << pos << " " << one_section << " " << before << " " << next << " " << b_n_section_time << " " << b_now_time << endl;
                //cout << "pos : " << pos << endl;
            }

            //py::object FileSystem = py::extract<py::object>(py_out_func["FileSystem"]);

            //string effect_id =

            // if (cpp == "py"){
            cout << "effect_plugin_elements" << endl;
            py::object effect_plugin_elements = py::extract<py::object>(py_out_func["EffectPluginElements"](effect_draw_base, effect_id, effect_value, first_value, before_value, next_value, various_fixed, now_frame, b_now_time, editor, python_operation, installation_sta, installation_end));
            cout << "procedure_return" << endl;
            py::object main_function = procedure.attr("main");
            cout << "procedure_return2" << endl;
            py::tuple procedure_return = py::extract<py::tuple>(main_function(effect_plugin_elements));

            cout << "effect終了" << endl;

            return procedure_return;
        }
    };
}
