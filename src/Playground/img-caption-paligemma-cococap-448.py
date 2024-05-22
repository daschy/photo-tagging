import os
import asyncio
from transformers import (
  PaliGemmaForConditionalGeneration,
  PaliGemmaProcessor,
)
from PIL import Image

# login(os.environ.get("HF_TOKEN"))

model_id = "google/paligemma-3b-ft-cococap-448"
model: PaliGemmaForConditionalGeneration = (
  PaliGemmaForConditionalGeneration.from_pretrained(
    model_id,
    token=os.environ.get("HF_TOKEN"),
  )
)
processor: PaliGemmaProcessor = PaliGemmaProcessor.from_pretrained(model_id)


def answer_question(image_path, prompt):
  with Image.open(image_path) as image:
    model_inputs = processor(
      text=prompt,
      images=image,
      return_tensors="pt",
    ).to("cpu")
    input_len = model_inputs["input_ids"].shape[-1]

    # with torch.inference_mode():
    generation = model.generate(
      **model_inputs,
      max_new_tokens=100,
      do_sample=False,
    )
    generation = generation[0][input_len:]
    decoded = processor.decode(
      generation,
      skip_special_tokens=True,
    )

  return decoded


async def main():
  # img_path = "/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_1759.NEF"
  img_path = "/Users/1q82/offline/ZDS_2942_DxO.jpg"
  # prompt = "what are the three main color of the photo?"
  prompt = "caption"
  captions = answer_question(img_path, prompt)
  print(f"{captions}")


if __name__ == "__main__":
  asyncio.run(main())
