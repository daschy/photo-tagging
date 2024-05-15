import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

class AI:
    def __init__(self, processor, model, tokenizer=None):
        self.processor = processor
        self.model = model
        self.model.to(device)
        self.tokenizer = tokenizer
        self.device = device