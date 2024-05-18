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
    entities = model.predict_entities(
        text=text, labels=_labels, multi_label=False, threshold=0.5
    )
    return entities


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
    text = "A man sits on a blanket in a park, basking in the clear blue sky. The park is filled with people, some lounging on blankets, others riding bikes. The man has long hair and is wearing sunglasses and a black jacket. A red"
    labels = ["object", "person"]
    entities = _getEntities(text, labels=labels)
    log.info(f"entities {[entity['text'] for entity in entities]}")
    # tokens = _merge_entities(text, entities)
    # log.info(f"merged {[token['text'] for token in tokens]}")
    text = "brown white and Jack"
    labels = ["color"]
    entities = _getEntities(text, labels=labels)
    log.info(f"entities {[entity['text'] for entity in entities]}")
    # tokens = _merge_entities(text, entities)
    # log.info(f"merged {[token['text'] for token in tokens]}")
    


if __name__ == "__main__":
    asyncio.run(main())
