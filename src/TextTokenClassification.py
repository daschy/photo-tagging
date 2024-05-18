from gliner import GLiNER
from typing import List
from Utils.LoggerUtils import GetLogger
import asyncio

log = GetLogger(__name__)
log.debug("Start init AI")
model = GLiNER.from_pretrained("numind/NuNerZero")
log.debug("End init AI")


def _getEntities(text: str, labels: List[str]) -> List[str]:
    _labels = [label.lower() for label in labels]
    entities = model.predict_entities(text, _labels)
    return entities


def _merge_entities(text:str, entities):
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
    output = [{'text': item['text'], 'score': item['score']} for item in merged]
    return output

async def main():
    text = "red and green and magenta on the grass"
    labels = ["color", "noun"]
    entities = _getEntities(text, labels=labels)
    tokens = _merge_entities(text, entities)
    log.info(f"{tokens}")


if __name__ == "__main__":
    asyncio.run(main())
