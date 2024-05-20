import unittest
from unittest.mock import patch
from src.Utils.TextTokenClassificationBert import TextToTokenList, LABELS, Token


class TestTextTokenClassificationBert(unittest.TestCase):
  @patch("caption_generator.token_classifier")
  async def test_textToTokens(self, mock_token_classifier):
    # Mock token_classifier return value
    mock_token_classifier.return_value = [
      {"word": "black", "score": 0.99, "entity_group": "ADJ"},
      {"word": "white", "score": 0.98, "entity_group": "ADJ"},
      {"word": "man", "score": 0.97, "entity_group": "NOUN"},
    ]

    # Call the textToTokens function with label ADJ
    result_adj = await TextToTokenList("black white man", LABELS.ADJ)

    # Assertions for ADJ
    expected_adj = [
      Token(text="black", score=0.99, label=["entity_group"]),
      Token(text="white", score=0.98, label=["entity_group"]),
    ]
    self.assertEqual(result_adj, expected_adj)

    # Call the textToTokens function with label NOUN
    result_noun = await TextToTokenList("black white man", LABELS.NOUN)

    # Assertions for NOUN
    expected_noun = [Token(text="man", score=0.97, label=["entity_group"])]
    self.assertEqual(result_noun, expected_noun)


if __name__ == "__main__":
  unittest.main()
