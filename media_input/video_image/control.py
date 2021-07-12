from media_input.video_image import image
from media_input.video_image import video

class Control_Video_Image:
    def __init__(self):
        self.iamge_class = {}
        self.video_class = {}

    def image_add(self,name,path):
        if name in list(self.iamge_class.keys()):
            return

        new = image.Video_Image_Stack()
        self.iamge_class[name] = new
        self.iamge_class[name].video_image_import(path)

    def video_add(self,name,path):
        if name in list(self.video_class.keys()):
            return

        new = video.Video_Image_Stack()
        self.video_class[name] = new
        self.video_class[name].video_image_import(path)

    def image_get(self,name):
        if not name in list(self.iamge_class.keys()):
            return

        px = self.iamge_class[name].video_image_get()
        return px

    def video_get(self,name,frame):
        if not name in list(self.video_class.keys()):
            return

        px = self.video_open[name].video_image_get(frame)
        return px




