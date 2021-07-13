from media_input.video_image import image
from media_input.video_image import video

class Control_Video_Image:
    def __init__(self):
        self.iamge_class = {}
        self.video_class = {}

    def image_add(self,path):
        if path in list(self.iamge_class.keys()):
            return

        new = image.Video_Image_Stack()
        self.iamge_class[path] = new
        self.iamge_class[path].video_image_import(path)

    def video_add(self,path):
        if path in list(self.video_class.keys()):
            return

        new = video.Video_Image_Stack()
        self.video_class[path] = new
        self.video_class[path].video_image_import(path)

    def image_get(self,path):
        if not path in list(self.iamge_class.keys()):
            return

        px = self.iamge_class[path].video_image_get()
        return px

    def video_get(self,path,frame):
        if not path in list(self.video_class.keys()):
            return

        px = self.video_open[path].video_image_get(frame)
        return px




