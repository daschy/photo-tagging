from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, TFAutoModelForSeq2SeqLM


tokenizer = AutoTokenizer.from_pretrained("t5-base")
# model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
model= TFAutoModelForSeq2SeqLM.from_pretrained("t5-base")

def translate(text, src_lang, tgt_lang):
    translator = pipeline(
        "translation_"+src_lang+"_to_"+tgt_lang,
        model=model,
        tokenizer=tokenizer,
        # src_lang=src_lang,
        # tgt_lang=tgt_lang,
    )
    translated_text = translator(text)
    return translated_text

print(translate("how are you?", "en", "de"))

# model = pipeline("text-generation")

# def predict(prompt):
#     completion = model(prompt)[0]["generated_text"]
#     return completion

# prediction = predict("My favorite programming language is")

# print(prediction)