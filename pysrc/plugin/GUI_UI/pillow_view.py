

class parts:
    def UI_set(self, UI_data):

        UI_data.edit_territory_position(x=0, y=0)
        UI_data.edit_territory_size(x=640, y=360)
        UI_data.new_diagram("TkImage_ground", diagram_type="TkImage")
        # UI_data.territory_draw()

        def size_update(width_size, height_size):
            pass

        def view(preview_image_tk):
            UI_data.diagram_draw("TkImage_ground", image_tk=preview_image_tk)
            return
            """
            image_pil = Image.fromarray(view_picture)  # RGBからPILフォーマットへ変換
            img_resize = image_pil
            if resize:
                img_resize = image_pil.resize((UI_data.canvas_size[0], UI_data.canvas_size[1]))
            image_tk = ImageTk.PhotoImage(image_pil)  # ImageTkフォーマットへ変換
            """

        UI_data.size_update = size_update
        UI_data.view = view

        return UI_data
