from Logger.LoggerUtils import GetLogger
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List
from transformers import (
    pipeline,
)
from Models.Token import Token
from enum import Enum

log = GetLogger(__name__)
log.debug("Start init AI")


# Token Classifier
token_classifier = pipeline(
    model="vblagoje/bert-english-uncased-finetuned-pos",
    aggregation_strategy="simple",
)

log.debug("End init AI")


class LABELS(Enum):
    NOUN = "NOUN"
    ADJ = "ADJ"


async def textToTokens(text: str, label: LABELS) -> List[Token]:
    loop = asyncio.get_running_loop()
    log.debug(f"Start tokenization {label.value}")
    with ThreadPoolExecutor() as pool:
        tokens = await loop.run_in_executor(
            pool,
            lambda:  token_classifier(text),
        )
        output = [
            Token(text=token["word"], score=token["score"], label=["entity_group"])
            for token in tokens
            if token["entity_group"] == (label.value)
        ]
    log.debug(f"End tokenization {label.value}")
    return output


async def main():
    text = "black white A man sits on a blanket in a park, basking in the clear blue sky. The park is filled with people, some lounging on blankets, others riding bikes. The man has long hair and is wearing sunglasses and a black jacket. A red"
    tokensAll = await asyncio.gather(
        textToTokens(text, LABELS.ADJ), textToTokens(text, LABELS.NOUN)
    )
    log.debug(f"{[token.text for token in tokensAll[0]]}")
    log.debug(f"{[token.text for token in tokensAll[1]]}")


if __name__ == "__main__":
    import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
    asyncio.run(main())