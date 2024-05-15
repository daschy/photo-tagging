from PIL import Image
import requests
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer

# Load the pre-trained model and tokenizer
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# Define the device to run the model on (e.g., "cpu" or "cuda")
device = "cpu"
model.to(device)

# Function to retrieve keywords from an image
def get_image_keywords(image_url):
    # Download the image
    image = Image.open(image_url)

    # Prepare the image for the model
    pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    # Generate the image caption
    output_ids = model.generate(pixel_values, max_length=50, num_beams=4, early_stopping=True)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # Extract keywords from the caption
    keywords = [word.lower() for word in caption.split() if word.isalnum()]

    return keywords

# Example usage
image_url = "/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_1759.NEF"
keywords = get_image_keywords(image_url)
print(keywords)