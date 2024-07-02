Python version 3.11.9 - pyenv "maildetector-venv" (developer info)

Model is based on MobileNet_V2 or MobileNet_Multi_Avg (as provided by mediapipe), and exported as a Tensorflow-Lite model. 
The model was trained on a dataset of ~125 images, ~1/3 for each class of "USPS", "UPS, and "Fedex" (images of delivery trucks + logos).
Trained for 30 epochs using mediapipe's model maker library. Default settings of batch_size: 8, learning_rate 0.3, cosine_decay_alpha: 1.0

The model takes a 256x256 input image, and outputs a set of points containing any identifieed classes.

I preformed post-training quantization to convert the model to 16-bit floating point, again using the mediapipe_model_maker library, to produce the model version titled {modelname}-fp16. From my understanding this version is more suited to GPU inference, will be testing on my Tesla GPU.

Inference time for the (non-quantized) MobileNet_V2 based model, on a single frame, running on an AMD Ryzen 5 2600 @ 3.400GHz, averages ~0.04s, taking up very little memory. For video inference on every frame of the input stream, this is fast enough to keep up with a 25fps stream on my machine.

Code is very messy, have fun updating it. Focusing on code quality for the actual implementation of this model. This is my first foray into cv model training, I roughly followed the documentation and guides at:
    - https://ai.google.dev/edge/mediapipe/solutions/vision/object_detector
    - https://ai.google.dev/edge/mediapipe/solutions/customization/object_detector
    - https://www.tensorflow.org/model_optimization/guide/quantization/post_training