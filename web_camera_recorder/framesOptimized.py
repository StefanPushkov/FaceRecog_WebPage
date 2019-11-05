import sys
import cv2
import config as cf
import pickle
import face_recognition
import imutils
import datetime
from subprocess import Popen, PIPE
import time

data = pickle.loads(open(cf.base_dir + '/EncodedFaces/EncodedFaces.pickle', "rb").read())
known_encodings, known_names = data['encodings'], data['names']

def StreamRecog():
    video = cv2.VideoCapture('rtsp://80.254.24.22:554')
    #video.set(cv2.CAP_PROP_FPS, 25)
    data = pickle.loads(open(cf.base_dir + '/EncodedFaces/EncodedFaces.pickle', "rb").read())
    known_encodings, known_names = data['encodings'], data['names']
    frame_counter = 0

    #['ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'yuv420', '-s', '1440x810', '-r', '25',
    #           '-i', 'pipe:0', '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-f', 'flv',
    #           'rtmp://78.46.97.176:1935/vasrc/faceTestInput']

    # Resized  1440x810, # Not resized 1920x1080
    p = Popen(['ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-s', '1920x1080',
               '-i', '-', '-c:v', 'libx264', '-crf', '20', '-preset', 'ultrafast', '-f', 'flv',
               'rtmp://78.46.97.176:1935/vasrc/ttty'], stdin=PIPE)
    frame_counter = 0
    while True:
        # Grab video frames
        ret, frame = video.read()
        frame_counter += 1
        if ret:
            if frame_counter % 5 == 0:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                frame = cv2.cvtColor(rgb, cv2.COLOR_BGR2YUV_I420)
                p.stdin.write(frame.tostring())

        else:
            break

    p.stdin.close()
    p.wait()
    video.release()
    cv2.destroyAllWindows()

StreamRecog()


# try:
#     video_stream()
# except BrokenPipeError as e:
#     pass

'''

import cv2
import subprocess as sp
import ffmpeg


cap = cv2.VideoCapture('rtsp://80.254.24.22:554')
ret_check, frame_check = cap.read()
height, width, ch = frame_check.shape


dimension = '{}x{}'.format(width, height)
f_format = 'bgr24' # remember OpenCV uses bgr format
fps = str(cap.get(cv2.CAP_PROP_FPS))


# ffmpeg -f rawvideo -pixel_format rgb24  -video_size 640x480 -i  "tcp://127.0.0.1:2345" -codec:v libx264 -pix_fmt yuv420p Video.mp4
command = [ffmpeg,
            '-f', 'rawvideo', '-pixel_format', 'yuv420p', '-video_size', dimension , f_format, '-i', 'rtsp://80.254.24.22:554', '-codec:v',
           'libx264', '-crf', '20', '-preset', 'veryfast', '-f', 'flv', 'http://localhost:7800']

proc = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    proc.stdin.write(frame.tostring().decode('utf-8'))

cap.release()
proc.stdin.close()
proc.stderr.close()
proc.wait()
'''