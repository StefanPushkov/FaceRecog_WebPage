import sys
import  cv2
import config as cf
import pickle
import face_recognition
import imutils
import datetime

def video_stream():

    video_camera = cv2.VideoCapture('rtsp://80.254.24.22:554')
    data = pickle.loads(open(cf.base_dir + '/EncodedFaces/EncodedFaces.pickle', "rb").read())
    known_encodings, known_names = data['encodings'], data['names']


    while True:
        ret, frame = video_camera.read()
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
            ret, rgb_resize = cv2.imencode('.jpg', rgb_resize)
            sys.stdout.write(rgb_resize.tostring())

        # sys.stdout.write(rgb_resize.tostring())
        # return rgb_resize.tostring()


        # else:
        #    yield (b'--frame\r\n'
        #           b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

video_stream()