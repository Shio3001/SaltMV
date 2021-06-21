import copy
# あくまでデータ保持のため


class UndoStack:
    def __init__(self, all_data):
        self.undo_stack_list = []
        self.undo_stack_list_now = 0
        self.all_data = all_data

        self.__safe = {"parameter": ["mov"],
                       "timelime_media": ["add", "mov", "del", "split", "lord"],
                       "timelime_keyframe": ["add", "mov", "del"],
                       "timelime_effect": ["add", "del"]
                       }

    def add_stack(self, media_id=None, effect_id=None, split_media_id=None, classification=None, add_type=None, func=None):
        if media_id is None:
            return

        if not classification in self.__safe.keys():
            return
        if not add_type in self.__safe[classification]:
            return

        undo = UndoStackData(self.all_data, media_id, effect_id, split_media_id, classification, add_type, func)
        self.undo_stack_list.append(undo)

        self.undo_stack_list_now = len(self.undo_stack_list)

    def confirmed_insert(self):
        self.undo_stack_list_now -= 1
        undo = self.undo_stack_list[self.undo_stack_list_now]
        self.all_data.media_object_had_layer(undo.media_id, undo.target_media_data)
        print("undo_obj", undo)
        undo.func(undo)


class UndoStackData:
    def __init__(self, all_data, media_id, effect_id, split_media_id, classification, add_type, func):
        self.all_data = all_data
        self.media_id = media_id
        self.effect_id = effect_id
        self.func = func

        self.classification = classification  # parameter , #timelime_media , # timelime_keyframe
        self.add_type = add_type  # add mov del
        self.target_media_data = self.all_data.media_object_had_layer(self.media_id)

        if not split_media_id is None:
            self.split_media_id = split_media_id
            self.target_media_data_split = self.all_data.media_object_had_layer(self.split_media_id)
