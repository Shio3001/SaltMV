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
                py::object this_object = py::list(object_group_values)[i];
                py::list installation = py::extract<py::list>(this_object[0].attr("installation"));
                int installation_sta = py::extract<float>(installation[0]);
                int installation_end = py::extract<float>(installation[1]);
                bool low = installation_sta <= frame;
                bool high = frame < installation_end;
                if (low && high)
                {
                    string layer_id = py::extract<string>(this_object[1]);
                    py::object layer_number_func = py_out_func["layer_number"];
                    int now_layer_number = py::extract<float>(layer_number_func(layer_id));
                    order_decision_object_group[now_layer_number] = this_object[0];
                    order_decision_object_group_number.push_back(now_layer_number);
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

            int editor_x = py::extract<float>(editor["x"]);
            int editor_y = py::extract<float>(editor["y"]);

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

            int installation_sta = py::extract<float>(installation[0]);
            int installation_end = py::extract<float>(installation[1]);

            vector<string> around_point_key = around_point_search(frame, id_time_key, id_time_value, installation_sta, installation_end);
            py::object effect_group = now_objcet.attr("effect_group"); //ここ  now_objcet  に effect_pointがあるわけないやろばか
            string synthetic_type = py::extract<string>(now_objcet.attr("synthetic"));
            EP::EffectProduction *effect_production = new EP::EffectProduction(frame, effect_group, py_out_func, python_operation, video_image_control, editor, around_point_key, effect_point_internal_id_time, installation_sta, installation_end);
            py::list effect_group_return = effect_production->production_effect_group();

            np::ndarray new_effect_draw = py::extract<np::ndarray>(effect_group_return[0]);
            py::list starting_point_center = py::extract<py::list>(effect_group_return[1]);

            py::tuple new_draw_size_shape = py::extract<py::tuple>(new_effect_draw.attr("shape"));
            int new_effect_draw_size[3];
            new_effect_draw_size[0] = py::extract<int>(new_draw_size_shape[1]); //y
            new_effect_draw_size[1] = py::extract<int>(new_draw_size_shape[0]); //x
            new_effect_draw_size[2] = py::extract<int>(new_draw_size_shape[2]); //r

            //new_effect_draw.attr("reshape")(-1);

            int effect_draw_size_multiplication = new_effect_draw_size[0] * new_effect_draw_size[1] * new_effect_draw_size[2];

            py::tuple shape_size = py::make_tuple(effect_draw_size_multiplication);
            np::ndarray new_effect_draw_1dimension = new_effect_draw.reshape(shape_size);

            py::tuple test_shape_size = py::extract<py::tuple>(new_effect_draw_1dimension.attr("shape"));

            int test_shape_size_int = py::extract<int>(test_shape_size[0]);
            cout << "test_shape_size_int " << test_shape_size_int << endl;

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
                int center = py::extract<float>(starting_point_center[i]);

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
            }

            cout << "synthetic_func" << endl;
            cout << "effect_draw_size_multiplication " << effect_draw_size_multiplication << endl;
            bool cpptype = python_operation["plugin"]["synthetic"][synthetic_type] == "TypeHppfileDefaultInclude";
            auto pointer_start = reinterpret_cast<int *>(new_effect_draw_1dimension.get_data());
            auto strides = new_effect_draw_1dimension.get_strides();
            //new_effect_draw_1dimension.get_data()

            //auto *start_pointer_numpy = reinterpret_cast<int *>(new_effect_draw_1dimension.get_data());

            cout << strides[0] << endl;
            //cout << strides[1] << endl;
            //cout << strides[2] << endl;

            cout << "cpptype" << cpptype << endl;
            int test = 0;
            if (cpptype)
            {

                cout << "add_draw_range_lu" << endl;
                cout << add_draw_range_lu[1] << endl;
                cout << add_draw_range_lu[0] << endl;
                cout << base_draw_range_rd[1] - base_draw_range_lu[1] << endl;
                cout << base_draw_range_rd[0] - base_draw_range_lu[0] << endl;

                int ya = add_draw_range_lu[1];
                for (int yb = base_draw_range_lu[1]; yb < base_draw_range_rd[1]; yb++)
                {
                    int xa = add_draw_range_lu[0];
                    for (int xb = base_draw_range_lu[0]; xb < base_draw_range_rd[0]; xb++)
                    {
                        int ipxA = (now_xy_size[0] * ya + xa) * 4;
                        int ipxB = (now_xy_size[0] * yb + xb) * 3;

                        float calculation[4];
                        float source[4];
                        float additions[4];

                        for (int i = 0; i < 3; i++)
                        {
                            source[i] = draw_object_draw_base[ipxB + i];
                        }
                        source[3] = 1;

                        for (int i = 0; i < 4; i++)
                        {
                            //additions[i] = 200;
                            //additions[i] = *start_pointer_numpy;
                            //start_pointer_numpy++;

                            int ipx = (ya * new_effect_draw_size[0] + xa) * new_effect_draw_size[2] + i;

                            cout << xa << " " << ya << " " << i << " " << ipx << endl;

                            int *this_draw = pointer_start + ipx;
                            additions[i] = *this_draw;
                        }

                        //additions[i] *= 1 / 255;
                        additions[3] = 1;

                        float *return_calculation;
                        if (synthetic_type == "normal")
                        {
                            return_calculation = synthetic_normal.run(calculation, source, additions);
                        }

                        float A = return_calculation[3];
                        int R = return_calculation[0] * A; //透明度反映
                        int G = return_calculation[1] * A;
                        int B = return_calculation[2] * A;

                        draw_object_draw_base[ipxB + 0] = R;
                        draw_object_draw_base[ipxB + 1] = G;
                        draw_object_draw_base[ipxB + 2] = B;
                        xa++;
                    }
                    ya++;
                }
            }
            else
            {
            }

            cout << "synthetic_func2" << endl;
        }

        vector<string> around_point_search(int frame, py::list &id_time_key, py::list &id_time_value, int installation_sta, int installation_end)
        {
            vector<string> around_point{"", ""};

            int id_time_len = py::len(id_time_key);
            bool frag_low = false;
            int low_frame = 0;
            for (int i = 0; i < id_time_len; i++) //低い値
            {
                int target = py::extract<float>(id_time_value[i]);
                if (target >= low_frame && target <= frame) //ここの条件式を直さないといけない
                {
                    around_point[0] = py::extract<string>(id_time_key[i]);
                    low_frame = py::extract<float>(id_time_value[i]);
                }
            }

            bool frag_high = false;
            int high_frame = py::extract<float>(editor["len"]);
            for (int i = 0; i < id_time_len; i++) //大きいあたい
            {
                int target = py::extract<float>(id_time_value[i]);
                if (target <= high_frame && target > frame)
                {
                    around_point[1] = py::extract<string>(id_time_key[i]);
                    high_frame = py::extract<float>(id_time_value[i]);
                    //cout << "around_point[1] " << around_point[1] << endl;
                }
                else if (frame == installation_end)
                {
                    around_point[1] = "default_end";
                    high_frame = py::extract<float>(id_time_value[i]);
                    //cout << "around_point[1] " << around_point[1] << endl;
                }
            }

            return around_point;
        }
    };
}