import gradio as gr
from transformers import AutoProcessor, AutoTokenizer, AutoImageProcessor, AutoModelForCausalLM, BlipForConditionalGeneration, VisionEncoderDecoderModel
import torch
from PIL import Image
from prettyprinter import cpprint as pp
import requests

# torch.hub.download_url_to_file('http://images.cocodataset.org/val2017/000000039769.jpg', './cats.jpg')
# torch.hub.download_url_to_file('https://huggingface.co/datasets/nielsr/textcaps-sample/resolve/main/stop_sign.png', './stop_sign.png')
# torch.hub.download_url_to_file('https://cdn.openai.com/dall-e-2/demos/text2im/astronaut/horse/photo/0.jpg', './astronaut.jpg')

git_processor_base = AutoProcessor.from_pretrained("microsoft/git-base-coco")
git_model_base = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco")

git_processor_large = AutoProcessor.from_pretrained("microsoft/git-large-coco")
git_model_large = AutoModelForCausalLM.from_pretrained("microsoft/git-large-coco")

blip_processor_base = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model_base = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

blip_processor_large = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
blip_model_large = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

vitgpt_processor = AutoImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
vitgpt_model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
vitgpt_tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = "cuda" if torch.cuda.is_available() else "cpu"

git_model_base.to(device)
blip_model_base.to(device)
git_model_large.to(device)
blip_model_large.to(device)
vitgpt_model.to(device)



def generate_caption(processor, model, image, tokenizer=None):
    inputs = processor(images=image, return_tensors="pt", ).to(device)
    
    generated_ids = model.generate(pixel_values=inputs.pixel_values, max_length=100)

    if tokenizer is not None:
        generated_caption = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    else:
        generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
   
    return generated_caption

def generate_captions(image):
    caption_git_base = [git_model_base.name_or_path, generate_caption(git_processor_base, git_model_base, image)]

    caption_git_large = [git_model_large.name_or_path, generate_caption(git_processor_large, git_model_large, image)]

    caption_blip_base = [blip_model_base.name_or_path, generate_caption(blip_processor_base, blip_model_base, image)]

    caption_blip_large = [blip_model_large.name_or_path, generate_caption(blip_processor_large, blip_model_large, image)]

    caption_vitgpt = [vitgpt_model.name_or_path, generate_caption(vitgpt_processor, vitgpt_model, image, vitgpt_tokenizer)]

    return caption_git_base, caption_git_large, caption_blip_base, caption_blip_large, caption_vitgpt


# url = 'https://piratediffusion.com/wp-content/uploads/sites/2/2023/11/photo_2023-11-14_10-35-12.jpg'
# image = Image.open(requests.get(url, stream=True).raw)

image =Image.open('/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_1759.NEF')

pp(generate_captions(image=image))
