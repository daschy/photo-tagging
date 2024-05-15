from ImageCaptionGenerate import device


class AI:
    def __init__(self, processor, model, tokenizer=None):
        self.processor = processor
        self.model = model
        self.model.to(device)
        self.tokenizer = tokenizer