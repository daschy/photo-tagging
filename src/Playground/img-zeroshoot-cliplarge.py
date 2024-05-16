from transformers import pipeline

# More models in the model hub.
model_name = "openai/clip-vit-large-patch14-336"
classifier = pipeline("zero-shot-image-classification", model=model_name)
image_to_classify = "path_to_cat_and_dog_image.jpeg"
labels_for_classification = ["cat and dog", "lion and cheetah", "rabbit and lion"]


scores = classifier(image_to_classify, candidate_labels=labels_for_classification)
print(scores)