

class parts:
    def UI_set(self, data):

        data.edit_territory_position(x=0, y=0)
        data.edit_territory_size(x=640, y=360)
        data.new_diagram("Matplotlib_ground", diagram_type="MatplotlibImage")
        # data.territory_draw()

        def size_update(width_size, height_size):
            pass

        def view(preview_image_tk):
            data.diagram_draw("Matplotlib_ground", image_tk=preview_image_tk)
            return
            """
            image_pil = Image.fromarray(view_picture)  # RGBからPILフォーマットへ変換
            img_resize = image_pil
            if resize:
                img_resize = image_pil.resize((data.canvas_size[0], data.canvas_size[1]))
            image_tk = ImageTk.PhotoImage(image_pil)  # ImageTkフォーマットへ変換
            """

        data.size_update = size_update
        data.view = view

        return data
