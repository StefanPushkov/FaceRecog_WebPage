
# import packages
from PIL import Image
from subprocess import Popen, PIPE
from imutils.video import VideoStream
from imutils.object_detection import non_max_suppression
from imutils import paths
import cv2
import numpy as np
import imutils

# ffmpeg setup

video = cv2.VideoCapture('rtsp://80.254.24.22:554')
r, cap = video.read()
print(str(cap.get(cv2.CAP_PROP_FPS)))

p = Popen(['ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-s', '1440x810', '-r', '25',
           '-i', 'pipe:0', '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-f', 'flv',
           'rtmp://78.46.97.176:1935/vasrc/faceTestInput'], stdin=PIPE)
while True:
    ret, frame = video.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV_I420)
        p.stdin.write(frame.tostring())
        # im = Image.fromarray(frame)
        # im.save(p.stdin, 'YUV420')
    else:
        break

p.stdin.close()
p.wait()
video.release()
cv2.destroyAllWindows()