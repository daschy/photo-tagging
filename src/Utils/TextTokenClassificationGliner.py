from gliner import GLiNER
from typing import List
import asyncio
from concurrent.futures import ThreadPoolExecutor
 
from src.Utils.LoggerUtils import GetLogger
from src.Models.Token import Token

log = GetLogger(__name__)
log.debug("Start init AI")
model = GLiNER.from_pretrained("numind/NuNerZero")
log.debug("End init AI")


async def textToTokens(text: str, labels: List[str]) -> List[Token]:
    _labels = [label.lower() for label in labels]
    loop = asyncio.get_running_loop()
    log.debug(f"Start tokenization {labels}")
    with ThreadPoolExecutor() as pool:
        entities = await loop.run_in_executor(
            pool,
            lambda: model.predict_entities(
                text=text, labels=_labels, multi_label=False, threshold=0.5
            ),
        )
    output = [
        Token(text=token["text"], score=token["score"], label=token["label"])
        for token in entities
    ]
    log.debug(f"End tokenization {labels}")
    return output


def _merge_entities(text: str, entities):
    if not entities:
        return []
    merged = []
    current = entities[0]
    for next_entity in entities[1:]:
        if next_entity["label"] == current["label"] and (
            next_entity["start"] == current["end"] + 1
            or next_entity["start"] == current["end"]
        ):
            current["text"] = text[current["start"] : next_entity["end"]].strip()
            current["end"] = next_entity["end"]
        else:
            merged.append(current)
            current = next_entity
    # Append the last entity
    merged.append(current)
    output = [{"text": item["text"], "score": item["score"]} for item in merged]
    return output


async def main():
    text = "brown white and Jack A man sits on a blanket in a park, basking in the clear blue sky. The park is filled with people, some lounging on blankets, others riding bikes. The man has long hair and is wearing sunglasses and a black jacket. A red"
    tokensAll = await asyncio.gather(
        textToTokens(text, labels=["object", "person"]),
        textToTokens(text, labels=["color"]),
    )
    log.info(f"{[token.text for token in tokensAll[0]]}")
    log.info(f"{[token.text for token in tokensAll[1]]}")


if __name__ == "__main__":
    asyncio.run(main())
