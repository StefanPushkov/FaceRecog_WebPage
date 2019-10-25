import cv2
import threading
import imutils
import face_recognition
import config as cf
import datetime
import pickle
import os

class RecordingThread (threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))

        if not os.path.exists(cf.base_dir + '/DB_csv'):
            os.makedirs(cf.base_dir + '/DB_csv')
            with open(cf.base_dir + '/DB_csv/records.csv', 'a') as f:
                f.write("Person; Time")
                f.write("\n")

    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()

class VideoCamera(object):
    data = pickle.loads(open(cf.base_dir + '/EncodedFaces/EncodedFaces.pickle', "rb").read())

    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture('rtsp://80.254.24.22:554') # rtsp://192.168.10.165:554
      
        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        num_frames = 20
        data = pickle.loads(open(cf.base_dir + '/EncodedFaces/EncodedFaces.pickle', "rb").read())
        known_encodings, known_names = data['encodings'], data['names']
        for i in range(0, num_frames):
            ret, frame = self.cap.read()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_resize = imutils.resize(rgb, width=1050)

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

            if ret:
                ret, jpeg = cv2.imencode('.jpg', rgb_resize)

                # Record video
                # if self.is_record:
                #     if self.out == None:
                #         fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                #         self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))

                #     ret, frame = self.cap.read()
                #     if ret:
                #         self.out.write(frame)
                # else:
                #     if self.out != None:
                #         self.out.release()
                #         self.out = None

                return jpeg.tobytes()

            else:
                return None

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()

            