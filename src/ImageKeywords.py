from transformers import (
    logging,
    pipeline,
    AutoTokenizer,
    AutoModelForTokenClassification,
)
from typing import List, Set
from prettyprinter import cpprint as pp


def _extract_keywords_from_caption(caption):
    token_classifier = pipeline(
        model="vblagoje/bert-english-uncased-finetuned-pos",
        aggregation_strategy="simple",
    )
    # token_classifier("My name is Sarah and I live in London")

    # token_classifier = pipeline(model="dslim/bert-base-NER-uncased", aggregation_strategy="simple" )
    sentence = caption
    tokens = token_classifier(sentence)
    nouns = [token["word"] for token in tokens if token["entity_group"] == "NOUN"]
    return nouns


def captionListToKeywords(captionList: List[str]) -> List[str]:
    merged_array = []
    for caption in captionList:
        keywords: List[str] = _extract_keywords_from_caption(caption)
        merged_array.extend(keywords)
    return list(set(merged_array))


# image_path = '/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_1759.NEF'
# image_to_text_pipeline = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
image_caption = "a woman sitting on a grassy field with a bunch of people"  # image_to_text_pipeline(image)[0]['generated_text']
keywords = captionListToKeywords([image_caption, "man in the middle"])
pp(keywords)
# pp(extract_keywords(imgPath))
# pp(tokens_noun)


# image = Image.fromarray(np.uint8(image)).convert("RGB")
# image.show()
