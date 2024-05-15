

import hashlib

def generate_file_fingerprint(file_path):
    try:
        with open(file_path, "rb") as f:
            file_contents = f.read()
            file_hash = hashlib.sha256(file_contents).hexdigest()
            return file_hash
    except FileNotFoundError:
        raise print("File not found!")
    except PermissionError:
        print(f"Error: Permission denied to access file '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while generating the fingerprint: {e}")
