import copy
# あくまでデータ保持のため


class UndoStack:
    def __init__(self, edit_control_auxiliary):
        self.undo_stack_list = []
        self.undo_stack_list_now = 0
        self.edit_control_auxiliary = edit_control_auxiliary

        self.__safe = {"parameter": ["mov"],
                       "timelime_media": ["add", "mov", "del", "split", "lord"],
                       "timelime_keyframe": ["add", "mov", "del", "lord"],
                       "timelime_effect": ["effect_add", "effect_del"]
                       }

    def del_stack(self, num=-1):

        if num < 0:
            num = self.undo_stack_list_now if self.undo_stack_list_now >= 0 else 0

        #print(self.undo_stack_list_now, "から削除")

        #print("削除前", self.undo_stack_list)
        del self.undo_stack_list[num:]
        #print("削除後", self.undo_stack_list)
        self.undo_stack_list_now = len(self.undo_stack_list)

    def all_del_stack(self):
        self.undo_stack_list = []
        self.undo_stack_list_now = 1

    def stop_once_add(self, undo, split_media_id=None):
        if not split_media_id is None:
            undo.set_split_media(split_media_id)

        print("[ add] ", undo.media_id, undo.classification, undo.add_type)
        self.undo_stack_list.append(undo)
        self.undo_stack_list_now = len(self.undo_stack_list)

    def add_stack(self, stop_once=None, media_id=None, effect_id=None, classification=None, add_type=None, func=None):
        if not classification in self.__safe.keys():
            return
        if not add_type in self.__safe[classification]:
            return

        #print(self.edit_control_auxiliary, media_id, effect_id, classification, add_type, func)
        undo = UndoStackData(self.edit_control_auxiliary, media_id, effect_id, classification, add_type, func)
        if stop_once:
            return undo, self.stop_once_add

        self.stop_once_add(undo)

        #print("undo_add", self.undo_stack_list_now, self.undo_stack_list)

    def confirmed_insert(self):
        self.undo_stack_list_now -= 1
        #print(self.undo_stack_list_now, self.undo_stack_list)

        if len(self.undo_stack_list) == 0:
            return

        if self.undo_stack_list_now < 0:
            self.undo_stack_list_now = 0

        if self.undo_stack_list_now > len(self.undo_stack_list) - 1:
            self.undo_stack_list_now = len(self.undo_stack_list) - 1

        undo = self.undo_stack_list[self.undo_stack_list_now]
        # if not undo.media_id is None:

        #print("******************************************undo_obj", undo.classification, undo.add_type, undo.media_id, undo.func)
        print("[ confirmed_insert ]", undo.media_id, undo.classification, undo.add_type)
        undo.func(undo)

        self.del_stack()

        # self.del_stack()


class UndoStackData:
    def __init__(self, edit_control_auxiliary, media_id, effect_id, classification, add_type, func):
        self.edit_control_auxiliary = edit_control_auxiliary
        self.media_id = media_id
        self.effect_id = effect_id
        self.func = func

        self.classification = classification  # parameter , #timelime_media , # timelime_keyframe
        self.add_type = add_type  # add mov del

        if not self.media_id is None:
            self.target_media_data = copy.deepcopy(self.edit_control_auxiliary.media_object_had_layer(self.media_id))
            self.media_id_key_frame = copy.deepcopy(self.target_media_data[0].effect_point_internal_id_time)

            #print("undo登録 : ", self.media_id_key_frame)

        # if not split_media_id is None:

    def set_split_media(self, split_media_id):
        self.split_media_id = split_media_id
        self.target_media_data_split = copy.deepcopy(self.edit_control_auxiliary.media_object_had_layer(self.split_media_id))
        self.split_media_id_key_frame = copy.deepcopy(self.target_media_data_split[0].effect_point_internal_id_time)

        #print("undo split 登録 : ", self.split_media_id_key_frame)
