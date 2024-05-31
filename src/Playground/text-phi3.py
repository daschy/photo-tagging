import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, AutoProcessor
from huggingface_hub import InferenceClient

torch.random.manual_seed(0)

model = AutoModelForCausalLM.from_pretrained(
	"microsoft/Phi-3-mini-4k-instruct",
	device_map="cpu",
	torch_dtype="auto",
	trust_remote_code=True,
)
tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
processor = AutoProcessor.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

messages = [
	{
		"role": "user",
		"content": "Can you provide ways to eat combinations of bananas and dragonfruits?",
	},
	{
		"role": "assistant",
		"content": "Sure! Here are some ways to eat bananas and dragonfruits together: 1. Banana and dragonfruit smoothie: Blend bananas and dragonfruits together with some milk and honey. 2. Banana and dragonfruit salad: Mix sliced bananas and dragonfruits together with some lemon juice and honey.",
	},
	{"role": "user", "content": "What about solving an 2x + 3 = 7 equation?"},
]

pipe = pipeline(
	"image-to-text",
	model=model,
	tokenizer=tokenizer,
	image_processor=processor,
)

generation_args = {
	"max_new_tokens": 50,
	"return_full_text": False,
	# "temperature": 5.0,
	"do_sample": False,
}

output = pipe(messages, **generation_args)
print(output[0]["generated_text"])
