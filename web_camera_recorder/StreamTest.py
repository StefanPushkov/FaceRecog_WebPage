import cv2


class VideoCamera(object):
    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture(0)  # rtsp://192.168.10.165:554

        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        print('Get')
        ret, frame = self.cap.read()

        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

        else:
            return None

def video_stream():
    global video_camera
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame()
        print('byte')
        if frame != None:
            global_frame = frame
            print('Op Byte thread!')
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')


def video_viewer():
    print("a")
    return video_stream()

while True:
    video_viewer()