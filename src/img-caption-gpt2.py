from transformers import pipeline
from PIL import Image
import requests

url = "http://images.cocodataset.org/val2017/000000039769.jpg"

image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

print(image_to_text(url))




# image = Image.fromarray(np.uint8(image)).convert("RGB")
# image.show()
