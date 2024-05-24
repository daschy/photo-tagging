Sure! Here's a README file for your project:

```markdown
# Photo Tagging

Photo Tagging is a Python project that allows you to read and write EXIF metadata in NEF (Nikon Electronic Format) files asynchronously using ExifTool. This project includes functionalities to add keywords to the EXIF metadata of NEF files, read all EXIF fields, and calculate file fingerprints before and after modification.

## Features

- Asynchronously add keywords to EXIF metadata in NEF files
- Asynchronously read all EXIF fields from NEF files
- Calculate file fingerprints (SHA-256) before and after modification

## Prerequisites

- Python 3.7 or later
- ExifTool installed on your system

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/daschy/photo-tagging.git
   cd photo-tagging
   ```

2. **Install the required Python packages:**

   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Adding Keywords to EXIF Metadata

To add keywords to the EXIF metadata of a NEF file asynchronously:

1. **Modify `main` function in `photo_tagging.py`:**

   ```python
   async def main():
       file_path = "path/to/your/image.nef"
       keywords = ["keyword1", "keyword2", "keyword3"]

       try:
           # Calculate fingerprint before modification
           fingerprint_before = calculate_file_fingerprint(file_path)
           print(f"Fingerprint before: {fingerprint_before}")

           # Add keywords to NEF EXIF
           await add_keywords_to_exif(file_path, keywords)

           # Calculate fingerprint after modification
           fingerprint_after = calculate_file_fingerprint(file_path)
           print(f"Fingerprint after: {fingerprint_after}")

           # Verify keywords are added
           exif_data = await read_all_exif_fields(file_path)
           print(f"EXIF data read from '{file_path}':")
           for key, value in exif_data.items():
               print(f"{key}: {value}")

           print(f"Keywords '{keywords}' added to {file_path}")
       except Exception as e:
           print(f"An error occurred: {e}")

   if __name__ == "__main__":
       asyncio.run(main())
   ```

2. **Run the script:**

   ```sh
   python photo_tagging.py
   ```

### Reading All EXIF Fields

To read all EXIF fields from a NEF file asynchronously:

1. **Call `read_all_exif_fields` function:**

   ```python
   async def main():
       file_path = "path/to/your/image.nef"

       try:
           # Read all EXIF fields
           exif_data = await read_all_exif_fields(file_path)
           print(f"EXIF data read from '{file_path}':")
           for key, value in exif_data.items():
               print(f"{key}: {value}")
       except Exception as e:
           print(f"An error occurred: {e}")

   if __name__ == "__main__":
       asyncio.run(main())
   ```

2. **Run the script:**

   ```sh
   python photo_tagging.py
   ```

### Calculating File Fingerprint

To calculate the SHA-256 fingerprint of a file:

1. **Use `calculate_file_fingerprint` function:**

   ```python
   file_path = "path/to/your/image.nef"
   fingerprint = calculate_file_fingerprint(file_path)
   print(f"File fingerprint: {fingerprint}")
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [ExifTool](https://exiftool.org/) by Phil Harvey for providing a powerful tool to manipulate EXIF metadata.
```

### Explanation:
- **Introduction**: Provides a brief overview of the project and its capabilities.
- **Features**: Lists the main functionalities.
- **Prerequisites**: Specifies the requirements to run the project.
- **Installation**: Details the steps to set up the project.
- **Usage**: Describes how to use the main features of the project, with code snippets and instructions.
- **Contributing**: Encourages contributions and explains how to contribute.
- **License**: States the licensing information.
- **Acknowledgements**: Credits the ExifTool for its contribution to the project.

You can place this README file in the root of your repository.