from transformers import pipeline
from torch.multiprocessing import Pool, Process, set_start_method

set_start_method("spawn", force=True)

model_name = "deepset/roberta-base-squad2"


PIPE = None


def get_pipe():
	# This will load the pipeline on demand on the current PROCESS/THREAD.
	# And load it only once.
	global PIPE
	if PIPE is None:
		PIPE = pipeline(
			"question-answering", model=model_name, tokenizer=model_name, device=-1
		)
	return PIPE


def get_answer(input_dict):
	reader = get_pipe()
	print("Input", input_dict)
	return reader(input_dict)


input_list = []
for i in range(3):
	QA_input = {"question": "This is a test", "context": "This is a context"}
	input_list.append(QA_input)

if __name__ == "__main__":
	result = []
	multi_pool = Pool(processes=3)
	predictions = multi_pool.map(get_answer, input_list)
	multi_pool.close()
	multi_pool.join()
	print(predictions)
