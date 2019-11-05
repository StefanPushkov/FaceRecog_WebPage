import sys
import cv2
import config as cf
import pickle
import face_recognition
import imutils
import datetime
import time

data = pickle.loads(open(cf.base_dir + '/EncodedFaces/EncodedFaces.pickle', "rb").read())
known_encodings, known_names = data['encodings'], data['names']

def video_stream():
    #video_camera = cv2.VideoCapture(0)
    time.sleep(2.0)
    video_camera = cv2.VideoCapture('rtsp://80.254.24.22:552')
    video_camera.set(cv2.CAP_PROP_FPS, 25)
    # video_camera = open_cam_rtsp("rtsp://170.93.143.139/rtplive/470011e600ef003a004ee33696235daa", 1920, 1080, 200)



    frame_counter = 0
    while True:
        # Grab video frames
        ret, frame = video_camera.read()
        frame_counter += 1
        if ret:
            if frame_counter % 5 == 0:

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # cv2.imshow('A', rgb_resize)
                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    break
                sys.stdout.write(str(rgb.tostring()))
    video_camera.release()
    cv2.destroyAllWindows()
    # ret, rgb_resize = cv2.imencode('.jpg', rgb_resize)
    # sys.stdout.write(str(rgb_resize.tostring()))

    # sys.stdout.write(rgb_resize.tostring())
    # return rgb_resize.tostring()


    # else:
    #    yield (b'--frame\r\n'
    #           b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

video_stream()

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