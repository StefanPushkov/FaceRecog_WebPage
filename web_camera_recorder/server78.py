from camera import VideoCamera

def video_stream():
    global video_camera
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # else:
        #    yield (b'--frame\r\n'
        #           b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

while True:
    video_stream()