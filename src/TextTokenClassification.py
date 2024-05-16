import torch
import transformers


model = transformers.AutoModel.from_pretrained(
    'numind/NuNER-multilingual-v0.1',
    output_hidden_states=True,
)
tokenizer = transformers.AutoTokenizer.from_pretrained(
    'numind/NuNER-multilingual-v0.1',
)

text = [
    "NuMind is an AI company based in Paris and USA.",
    "NuMind est une entreprise d'IA basée à Paris et aux États-Unis.",
    "See other models from us on https://huggingface.co/numind"
]
encoded_input = tokenizer(
    text,
    return_tensors='pt',
    padding=True,
    truncation=True
)
output = model(**encoded_input)

# two emb trick: for better quality
emb = torch.cat(
    (output.hidden_states[-1], output.hidden_states[-7]),
    dim=2
)
print(output)


# single emb: for better speed
# emb = output.hidden_states[-1]
