import os
import hashlib
import subprocess


def calculate_file_fingerprint(file_path):
  hash_func = hashlib.sha256()
  with open(file_path, "rb") as f:
    while chunk := f.read(8192):
      hash_func.update(chunk)
  return hash_func.hexdigest()


def add_keyword_to_exif(file_path, keyword):
  subprocess.run(["exiftool", f"-keywords={keyword}", file_path], check=True)
  # ExifTool creates a backup file with _original suffix, so remove it
  backup_file = f"{file_path}_original"
  if os.path.exists(backup_file):
    os.remove(backup_file)


if __name__ == "__main__":
  image_path = "/Users/Shared/projects/phototagging/milotagging/src/tests/test_data/person_walking_gps.NEF"
  keyword = "red1 green1 biking1 purple pippo pluto e anche madonna incoronata"

  # Calculate fingerprint before modification
  fingerprint_before = calculate_file_fingerprint(image_path)
  print(f"Fingerprint before: {fingerprint_before}")

  # Add keyword to NEF EXIF
  add_keyword_to_exif(image_path, keyword)

  # Calculate fingerprint after modification
  fingerprint_after = calculate_file_fingerprint(image_path)
  print(f"Fingerprint after: {fingerprint_after}")

  print(f"Keyword '{keyword}' added to {image_path}")
