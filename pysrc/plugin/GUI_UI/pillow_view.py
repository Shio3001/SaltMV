

class parts:
    def UI_set(self, UI_auxiliary):

        UI_auxiliary.edit_territory_position(x=0, y=0)
        UI_auxiliary.edit_territory_size(x=640, y=360)
        UI_auxiliary.new_diagram("TkImage_ground", diagram_type="TkImage")
        # UI_auxiliary.territory_draw()

        def size_update(width_size, height_size):
            UI_auxiliary.edit_territory_size(x=width_size, y=height_size)

        def view(preview_image_tk):
            UI_auxiliary.diagram_draw("TkImage_ground", image_tk=preview_image_tk)
            return
            """
            image_pil = Image.fromarray(view_picture)  # RGBからPILフォーマットへ変換
            img_resize = image_pil
            if resize:
                img_resize = image_pil.resize((UI_auxiliary.canvas_size[0], UI_auxiliary.canvas_size[1]))
            image_tk = ImageTk.PhotoImage(image_pil)  # ImageTkフォーマットへ変換
            """

        UI_auxiliary.size_update = size_update
        UI_auxiliary.view = view

        return UI_auxiliary
