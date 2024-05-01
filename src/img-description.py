from transformers import pipeline
from PIL import Image
import requests

url = "https://unsplash.com/photos/g8oS8-82DxI/download?ixid=MnwxMjA3fDB8MXx0b3BpY3x8SnBnNktpZGwtSGt8fHx8fDJ8fDE2NzgxMDYwODc&force=true&w=640"

image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

print(image_to_text(url))




# image = Image.fromarray(np.uint8(image)).convert("RGB")
# image.show()
