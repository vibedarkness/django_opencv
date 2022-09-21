from django.shortcuts import render
from django.views.decorators import gzip
from django.core.mail import EmailMessage
from django.http import StreamingHttpResponse,HttpResponse
import cv2
import threading

# Create your views here.
@gzip.gzip_page
def videovibe(request):
    try:
        cam=Videocamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")

    except:
        pass
    return render(request, 'video.html')


class Videocamera(object):
    def __init__(self):
        self.video=cv2.VideoCapture(0)
        (self.grabbed, self.frame)=self.video.read()
        threading.Thread(target=self.update, args=()).start()
    def __del__(self):
        self.video.release()
    def get_frame(self):
        image=self.frame
        _ , jpeg=cv2.imencode('.jpeg',image)
        return jpeg.tobytes()
    def update(self):
        while True:
            (self.grabbed, self.frame)=self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
        b'Content-Type : image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')