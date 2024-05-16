from transformers import (
    OneFormerProcessor,
    OneFormerForUniversalSegmentation,
    Mask2FormerImageProcessor,
    Mask2FormerForUniversalSegmentation,
)
from PIL import Image
import torch
from prettyprinter import cpprint as pp


def label_segmentation(model, segmentation, segments_info):
    output = list()
    for segment in segments_info:
        segment_label_id = segment["label_id"]
        segment_score = segment["score"]
        segment_label = model.config.id2label[segment_label_id]
        output.append({"label": segment_label, "score": segment_score})
    return sorted(output,key=lambda i: i['score'], reverse=True)


def load_model_and_processor(model_ckpt: str):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = Mask2FormerForUniversalSegmentation.from_pretrained(model_ckpt).to(torch.device(device))
    model.eval()
    image_preprocessor = Mask2FormerImageProcessor.from_pretrained(model_ckpt)
    return model, image_preprocessor


# processor = Mask2FormerImageProcessor.from_pretrained("shi-labs/oneformer_ade20k_swin_large")
# model = Mask2FormerForUniversalSegmentation.from_pretrained(
#     "shi-labs/oneformer_ade20k_swin_large"
# )

model, processor = load_model_and_processor('facebook/mask2former-swin-large-coco-panoptic')


image_path = "/Users/1q82/Pictures/Photos/Amsterdam/Nature/ZDS_2322.NEF"
image_path = "/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_2612.NEF"
image_path="/Users/1q82/Pictures/Photos/Amsterdam/Nature/ZDS_2276.NEF"
image = Image.open(image_path)

inputs = processor(image, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

prediction = processor.post_process_panoptic_segmentation(
    outputs, target_sizes=[image.size[::-1]]
)[0]

pp(label_segmentation(model, **prediction))
