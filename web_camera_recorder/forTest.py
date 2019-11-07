# import packages
from PIL import Image
from subprocess import Popen, PIPE
from imutils.video import VideoStream
from imutils.object_detection import non_max_suppression
from imutils import paths
import cv2
import datetime
import numpy as np
import imutils
import config as cf
import pickle
import face_recognition
# ffmpeg setup
def StreamRecog():
    video = cv2.VideoCapture('rtsp://80.254.24.22:554') # rtsp://192.168.10.165:554 # rtsp://80.254.24.22:554
    video.set(cv2.CAP_PROP_FPS, 25)
    data = pickle.loads(open(cf.base_dir + '/EncodedFaces/EncodedFaces.pickle', "rb").read())
    known_encodings, known_names = data['encodings'], data['names']
    frame_counter = 0

    #['ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-s', '1440x810', '-r', '25',
    #           '-i', 'pipe:0', '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-f', 'flv',
    #           'rtmp://78.46.97.176:1935/vasrc/faceTestInput']

    # Resized  1440x810, # Not resized 1920x1080
    p = Popen(['ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-s', '960x540',
               '-i', '-', '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-f', 'flv',
               'rtmp://78.46.97.176:1935/vasrc/ttty'], stdin=PIPE)
    while True:
        ret, frame = video.read()
        frame_counter += 1

        if ret:
            if frame_counter % 1:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb = imutils.resize(rgb, height=540, width=960)

                # Resize frame of video to 1/4 size for faster face recognition processing
                #rgb = cv2.resize(rgb, (0, 0), fx=0.5, fy=0.5)

                boxes = face_recognition.face_locations(rgb,
                                                        model='hog')

                encodings = face_recognition.face_encodings(rgb, boxes)
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
                    cv2.rectangle(rgb, (left, top), (right, bottom),
                                  (0, 255, 0), 2)
                    y = top - 15 if top - 15 > 15 else top + 15
                    cv2.putText(rgb, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                                0.75, (0, 255, 0), 2)

                yuv = cv2.cvtColor(rgb, cv2.COLOR_RGB2YUV_I420)
                p.stdin.write(yuv.tostring())
            # im = Image.fromarray(frame)
            # im.save(p.stdin, 'YUV420')
        else:
            break

    p.stdin.close()
    p.wait()
    video.release()
    cv2.destroyAllWindows()

StreamRecog()