class ChangeScene:
    def change(self, all_data, user_select):
        # Scene再描画イベント発火

        if len(all_data.scenes) >= user_select:
            all_data.now_scene = user_select
            all_data.operation["log"].write("シーンの変更は受け付けられました")

        else:
            all_data.operation["log"].write("シーンの変更は受け付けられませんでした")

        return all_data
