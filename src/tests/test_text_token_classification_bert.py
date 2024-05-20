import pytest
from typing import List
from src.utils.text_token_classification_bert import TextToTokenList, LABELS, Token
from src.tests.test_utils.assert_lists_of_objects_equal_ignore_attr import (
  assert_lists_of_objects_equal_ignore_attr,
)


# Using pytest's mark.asyncio to run async test cases
@pytest.mark.asyncio
async def test_text_to_token_list():
  text = "black and white canvas"

  # Assertions for ADJ
  expected_adj_list: List[Token] = [
    Token(text="black", score=0.99, label=LABELS.ADJ.value),
    Token(text="white", score=0.98, label=LABELS.ADJ.value),
  ]

  # Call the TextToTokenList function with label ADJ
  result_adj_list = await TextToTokenList(text, LABELS.ADJ)

  assert_lists_of_objects_equal_ignore_attr(expected_adj_list, result_adj_list, "score")

  # Call the TextToTokenList function with label NOUN
  result_noun_list = await TextToTokenList(text, LABELS.NOUN)

  # Assertions for NOUN
  expected_noun_list = [
    Token(text="canvas", score=0.97, label=LABELS.NOUN.value),
  ]

  assert_lists_of_objects_equal_ignore_attr(
    result_noun_list, expected_noun_list, "score"
  )


# If this script is executed directly, run pytest
if __name__ == "__main__":
  pytest.main()
