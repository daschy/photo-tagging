import os
from transformers import (
	PaliGemmaForConditionalGeneration,
	PaliGemmaProcessor,
	pipeline,
	AutoTokenizer,
)
from PIL import Image
import requests
from io import BytesIO


# Function to load an image from a URL
def load_image(img_url: str) -> Image.Image:
	# response = requests.get(img_url)
	img = Image.open(image_url)
	return img


# Initialize the model and processor
model_id = "google/paligemma-3b-ft-cococap-448"
model = PaliGemmaForConditionalGeneration.from_pretrained(model_id)
processor = PaliGemmaProcessor.from_pretrained(model_id, return_tensors="pt")
tokenizer = AutoTokenizer.from_pretrained(model_id)


# Example usage
if __name__ == "__main__":
	# Load an image
	image_url = "/Users/1q82/Pictures/Photos/Sport/Fencing/2022-NL-Camp/ZDS_3465.NEF"  # Replace with your image URL
	image = load_image(image_url)
	image_captioning_pipeline = pipeline(
		"image-to-text",
		model=model,
		image_processor=processor,
		tokenizer=tokenizer,
		device="cpu",
		model_kwargs=[
			processor(text="caption", images=image, return_tensors="pt"),
		],
	)
	# Generate and print the caption
	caption = image_captioning_pipeline([image])
	print("Generated Caption:", caption[0])
