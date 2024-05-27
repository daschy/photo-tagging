import re
import json


def read_sidecar_file(file_path):
	try:
		with open(file_path, "r", encoding="utf-8") as file:
			data = file.read()
			return data
	except FileNotFoundError:
		print(f"Error: The file {file_path} does not exist.")
		return None


def parse_sidecar_content(content):
	# This function will parse the given content line-by-line.
	def parse_value(value):
		# Try to convert to int, float, or keep as string
		try:
			return int(value)
		except ValueError:
			try:
				return float(value)
			except ValueError:
				if value == "true":
					return True
				elif value == "false":
					return False
				return value.strip('"')

	lines = content.split("\n")
	result = {}
	stack = [result]
	keys = []

	for line in lines:
		line = line.strip()
		if line.endswith("{"):
			# New dictionary starts
			key = line.split("=")[0].strip()
			if key:
				keys.append(key)
				stack[-1][key] = {}
				stack.append(stack[-1][key])
			else:
				stack.append({})
		elif line.endswith("},"):
			# Dictionary ends
			stack.pop()
		elif "=" in line:
			key, value = map(str.strip, line.split("=", 1))
			if value.endswith(","):
				value = value[:-1]
			stack[-1][key] = parse_value(value)
		elif line.endswith("},") or line.endswith("}"):
			stack.pop()

	return result


def print_parsed_data(data, indent=4):
	print(json.dumps(data, indent=indent))


def main():
	file_path = "/Users/Shared/projects/phototagging/milotagging/tests/test_data/DSC_4718.NEF.dop"  # Replace with your file path
	content = read_sidecar_file(file_path)
	if content:
		parsed_data = parse_sidecar_content(content)
		# print_parsed_data(parsed_data)
		print(parsed_data["Sidecar"]["Source"]["Items"]["{"]["GPSLatitude"])
		# print(parsed_data["Sidecar"]["Source"]["GPSLongitude"])


if __name__ == "__main__":
	main()
