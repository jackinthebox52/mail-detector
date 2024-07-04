import cv2
import sys

VIDEO_URL = "assets/truck-videos/ups-convoy/stream.m3u8"

cap = cv2.VideoCapture(VIDEO_URL)
if (cap.isOpened() == False):
    print('!!! Unable to open URL')
    sys.exit(-1)

# retrieve FPS and calculate how long to wait between each frame to be display
fps = cap.get(cv2.CAP_PROP_FPS)
wait_ms = int(1000/fps)
print('FPS:', fps)

count = 0

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        cv2.imwrite('assets/frame{:f}.jpg'.format(count), frame)
        count += fps/4 # i.e. at 30 fps, this advances one second
        cap.set(cv2.CAP_PROP_POS_FRAMES, count)
    else:
        cap.release()
        break