from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, PreTrainedTokenizerFast
from PIL import Image
import requests
from prettyprinter import cpprint as pp




model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
vit_feature_extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch16-224-in21k")
tokenizer = PreTrainedTokenizerFast.from_pretrained("distilgpt2")

def vit2distilgpt2(img):
    pixel_values = vit_feature_extractor(images=img, return_tensors="pt").pixel_values
    encoder_outputs = model.generate(pixel_values.to('cpu'), num_beams=10, num_return_sequences=1)
    generated_sentences = tokenizer.batch_decode(encoder_outputs, skip_special_tokens=True)

    return generated_sentences

url = 'http://images.cocodataset.org/val2017/000000039769.jpg'
image = Image.open(requests.get(url, stream=True).raw)

pp(vit2distilgpt2(image))