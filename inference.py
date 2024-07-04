#   https://www.tensorflow.org/lite/guide/inference#load_and_run_a_model_in_python

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2

MODEL_PATH = '/home/guthix/Projects/mail-detector/neuralnet/models/mobilenetV2_1/model.tflite'

BaseOptions = mp.tasks.BaseOptions
DetectionResult = mp.tasks.components.containers.DetectionResult
ObjectDetector = mp.tasks.vision.ObjectDetector
ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode

def print_result(result: DetectionResult, output_image: mp.Image, timestamp_ms: int):
    score = result.detections[0].categories[0].score
    clas = result.detections[0].categories[0].category_name
    if score >= 0.33:           #Heuristic percentage as confidence threshold
        print(f'(async callback) detection result: {clas} logo found, confidence {score}%')

options = ObjectDetectorOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.LIVE_STREAM,
    max_results=1,                  #Only return single object class as result, as mail truck deliveries rarely overlap (TODO: consider they could possibly overlap)
    result_callback=print_result)

with ObjectDetector.create_from_options(options) as detector:
    # The detector is initialized. Now we read our stream input with a loop

    # Use OpenCV’s VideoCapture to start capturing from the webcam.
    VIDEO_URL = "assets/truck-videos/ups-convoy/stream.m3u8"    #TODO get real stream as input
    cap = cv2.VideoCapture(VIDEO_URL)
    if (cap.isOpened() == False):
        print('!!! Unable to open URL')
        sys.exit(-1)

    # retrieve FPS and calculate how long to wait between each frame to be display
    fps = cap.get(cv2.CAP_PROP_FPS)
    wait_ms = int(1000/fps)
    print('FPS:', fps)
    count = 0
    frame_ms = 0
    # Create a loop to read the latest frame from the camera using VideoCapture#read()
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            # Convert the frame received from OpenCV to a MediaPipe’s Image object.
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

            # Send the latest frame to perform object detection.
            # Results are sent to the `result_callback` provided in the `ObjectDetectorOptions`.
            detector.detect_async(mp_image, frame_ms)
    
            #Skip forward 1/4 second
            count += fps/4 # i.e. at 30 fps, this advances one second
            frame_ms += int(count*250)   #TODO verify this
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)
        else:
            cap.release()
            break




 
