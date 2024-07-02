import os
import json
import tensorflow as tf
assert tf.__version__.startswith('2')

from mediapipe_model_maker import object_detector
train_dataset_path = "/home/guthix/Projects/mail-detector/neuralnet/dataset/COCO/training"
validation_dataset_path = "/home/guthix/Projects/mail-detector/neuralnet/dataset/COCO/testing"

with open(os.path.join(train_dataset_path, "labels.json"), "r") as f:
  labels_json = json.load(f)
for category_item in labels_json["categories"]:
  print(f"{category_item['id']}: {category_item['name']}")
  
train_data = object_detector.Dataset.from_coco_folder(train_dataset_path, cache_dir="/tmp/od_data/train")
validation_data = object_detector.Dataset.from_coco_folder(validation_dataset_path, cache_dir="/tmp/od_data/validation")
print("train_data size: ", train_data.size)
print("validation_data size: ", validation_data.size)


spec = object_detector.SupportedModels.MOBILENET_MULTI_AVG
hparams = object_detector.HParams(export_dir='/home/guthix/Projects/mail-detector/neuralnet/models/mobilenet_multi_avg_1')
options = object_detector.ObjectDetectorOptions(
    supported_model=spec,
    hparams=hparams
)

model = object_detector.ObjectDetector.create(
    train_data=train_data,
    validation_data=validation_data,
    options=options)

print(f'\nTrained model is complete. \n\nValidating the model...')

loss, coco_metrics = model.evaluate(validation_data, batch_size=4)
print(f"Validation loss: {loss}")
print(f"Validation coco metrics: {coco_metrics}\n\n Exporting the model...")

model.export_model()
