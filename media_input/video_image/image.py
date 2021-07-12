from PIL import Image, ImageFilter

class Video_Image_Stack:
    def __init__(self):
        self.new_image = None
        self.image_property = None

    def video_image_import(self,path):
        try:
            self.new_image = Image.open(path)
        except:
            print("読み込みに失敗 try - except")
        
        self.image_property = {"width": self.new_image.shape[1],
                                "height": self.new_image.shape[0]}

    def video_image_get(self,frame):
        return self.new_image

