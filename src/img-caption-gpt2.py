from transformers import logging,pipeline,AutoTokenizer,AutoModelForTokenClassification
from PIL import Image
import requests
from prettyprinter import cpprint as pp

logging.set_verbosity_warning()

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
# url = 'https://piratediffusion.com/wp-content/uploads/sites/2/2023/11/photo_2023-11-14_10-35-12.jpg'
# image = Image.open(requests.get(url, stream=True).raw)

image =Image.open('/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_1759.NEF')


image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
image_caption = image_to_text(image)[0]['generated_text']
pp(image_caption)


token_classifier = pipeline(model="vblagoje/bert-english-uncased-finetuned-pos", aggregation_strategy="simple")
# token_classifier("My name is Sarah and I live in London")

# token_classifier = pipeline(model="dslim/bert-base-NER-uncased", aggregation_strategy="simple" )
sentence = image_caption
tokens = token_classifier(sentence)
tokens_noun = [token for token in tokens if token["entity_group"] == "NOUN"]
words = [token['word'] for token in tokens if token["entity_group"] == "NOUN"]
pp([list(dict.fromkeys(words))])
pp(tokens_noun)






# image = Image.fromarray(np.uint8(image)).convert("RGB")
# image.show()
