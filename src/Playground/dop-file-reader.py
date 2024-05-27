import json
import os


def read_sidecar_file(file_path):
	try:
		with open(file_path, "r", encoding="utf-8") as file:
			data = file.read()
			return data
	except FileNotFoundError:
		print(f"Error: The file {file_path} does not exist.")
		return None


def parse_sidecar_content(content):
	def parse_value(value):
		try:
			return int(value)
		except ValueError:
			try:
				return float(value)
			except ValueError:
				if value.lower() == "true":
					return True
				elif value.lower() == "false":
					return False
				elif value.startswith('"') and value.endswith('"'):
					return value.strip('"')
				return value

	lines = content.split("\n")
	result = {}
	stack = [result]
	keys = []
	current_list = None

	for line in lines:
		line = line.strip()
		if line.endswith("{"):
			key = line.split("=")[0].strip()
			if key:
				keys.append(key)
				if key == "Items" or key == "HSLHueSlices" or key == "Keywords":
					new_list = []
					stack[-1][key] = new_list
					stack.append(new_list)
					current_list = new_list
				else:
					new_dict = {}
					if isinstance(stack[-1], list):
						stack[-1].append(new_dict)
					else:
						stack[-1][key] = new_dict
					stack.append(new_dict)
					current_list = None
			else:
				new_dict = {}
				stack[-1].append(new_dict)
				stack.append(new_dict)
		elif line.endswith("},") or line.endswith("}"):
			if isinstance(stack[-1], dict) and keys and keys[-1] == "Items":
				current_list = stack.pop()
			else:
				stack.pop()
			if keys:
				keys.pop()
		elif "=" in line:
			key, value = map(str.strip, line.split("=", 1))
			if value.endswith(","):
				value = value[:-1]
			parsed_value = parse_value(value)
			if isinstance(stack[-1], list):
				if not stack[-1] or not isinstance(stack[-1][-1], dict):
					stack[-1].append({})
				stack[-1][-1][key] = parsed_value
			else:
				stack[-1][key] = parsed_value

	return result


def save_to_json(data, output_path):
	with open(output_path, "w", encoding="utf-8") as json_file:
		json.dump(data, json_file, indent=4)


def main():
	file_path = f"{os.path.dirname(__file__)}/playground_data/DSC_4718.NEF.dop"
	output_path = f"{os.path.dirname(__file__)}/playground_data/output.json"  # Path for the output JSON file
	content = read_sidecar_file(file_path)
	if content:
		parsed_data = parse_sidecar_content(content)
		save_to_json(parsed_data, output_path)
		print(f"Successfully parsed and saved to {output_path}")


if __name__ == "__main__":
	main()
