import asyncio
from models.AIGenPaliGemma import AIGenPaliGemma
from models.AIGenBert import AIGenBert
from models.ReverseGeotaggingXMP import ReverseGeotaggingXMP
from models.StrategyGenerateKeywordList import StrategyGenerateKeywordList
from utils.PhotoTaggingProcessor import PhotoTaggingProcessor


async def main(root_dir: str):
	processor = PhotoTaggingProcessor()
	strategy = StrategyGenerateKeywordList(
		image_to_text_ai_list=[
			AIGenPaliGemma(
				model_id="google/paligemma-3b-ft-cococap-448",
				prompt="caption",
			),
			AIGenPaliGemma(
				model_id="google/paligemma-3b-ft-cococap-448",
				prompt="what are the four most dominant colors in the picture?",
			),
		],
		token_classification_ai=AIGenBert(
			model_id="vblagoje/bert-english-uncased-finetuned-pos",
		),
		reverse_geotagging=ReverseGeotaggingXMP(),
	)
	processor.set_strategy(strategy=strategy)

	await processor.execute(root_dir, dry_run=True)


if __name__ == "__main__":
	directory = "/Users/1q82/Pictures/Photos/SouthKorea"
	asyncio.run(main(directory))
