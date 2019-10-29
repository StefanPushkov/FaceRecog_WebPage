from camera import VideoCamera
import sys

def video_stream():

    video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame()


        sys.stdout.write(frame.tostring())
        # else:
        #    yield (b'--frame\r\n'
        #           b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

