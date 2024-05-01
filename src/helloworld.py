from transformers import pipeline
# import gradio as gr


model = pipeline("text-generation")

def predict(prompt):
    completion = model(prompt)[0]["generated_text"]
    return completion

prediction = predict("My favorite programming language is")
# demo = gr.Interface(fn=predict, inputs="text", outputs="text").launch(share=True)

print(prediction)