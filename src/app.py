import asyncio
from models.AIGenPretrained import AIGenPretrained
from models.AIGenPipeline import AIGenPipeline
from models.ReverseGeotaggingXMP import ReverseGeotaggingXMP
from models.StrategyGenerateKeywordList import StrategyGenerateKeywordList
from utils.PhotoTaggingProcessor import PhotoTaggingProcessor


async def main(root_dir: str):
	processor = PhotoTaggingProcessor()
	strategy = StrategyGenerateKeywordList(
		image_to_text_ai=AIGenPretrained(
			model_id="google/paligemma-3b-ft-cococap-448",
		),
		token_classification_ai=AIGenPipeline(
			model_id="vblagoje/bert-english-uncased-finetuned-pos",
		),
		reverse_geotagging=ReverseGeotaggingXMP(),
	)
	processor.set_strategy(strategy=strategy)

	await processor.execute(root_dir, dry_run=True)


if __name__ == "__main__":
	directory = "/Users/1q82/Pictures/Photos/Amsterdam"
	asyncio.run(main(directory))
