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
    video_camera = cv2.VideoCapture('rtsp://80.254.24.22:554')
    # video_camera = open_cam_rtsp("rtsp://170.93.143.139/rtplive/470011e600ef003a004ee33696235daa", 1920, 1080, 200)




    while True:
        # Grab video frames
        ret, frame = video_camera.read()
        if ret:
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize frame of video to 1/4 size for faster face recognition processing
            rgb_resize = cv2.resize(rgb, (0, 0), fx=0.75, fy=0.75)

            boxes = face_recognition.face_locations(rgb_resize,
                                                    model='hog')

            encodings = face_recognition.face_encodings(rgb_resize, boxes)
            names = []

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(known_encodings,
                                                         encoding)
                detection_at = datetime.datetime.now()
                name = "Unknown"

                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = known_names[i]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key=counts.get)

                    # update the list of names
                names.append(name)

                csv_line = name + ";" + str(detection_at)
                with open(cf.base_dir + '/DB_csv/records.csv', 'a') as outfile:
                    outfile.write(csv_line + "\n")
            for ((top, right, bottom, left), name) in zip(boxes, names):
                # rescale the face coordinates
                top = int(top)
                right = int(right)
                bottom = int(bottom)
                left = int(left)

                # draw the predicted face name on the image
                cv2.rectangle(rgb_resize, (left, top), (right, bottom),
                              (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(rgb_resize, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 255, 0), 2)

            rgb_resize = cv2.cvtColor(rgb_resize, cv2.COLOR_RGB2YUV_I420)
            # cv2.imshow('A', rgb_resize)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
            sys.stdout.write(str(rgb_resize.tostring()))
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