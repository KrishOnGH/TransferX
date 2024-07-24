import os

def process_file(file_path):
    if not os.path.isfile(file_path):
        return "Invalid file."

    directory, original_filename = os.path.split(file_path)
    original_extension = os.path.splitext(original_filename)[1]
    if not original_extension:
        new_filename = "abcd"
    else:
        new_filename = f"abcd{original_extension}"
    new_file_path = os.path.join(directory, new_filename)

    try:
        os.rename(file_path, new_file_path)
        return f"Renamed to {new_file_path}"
    except Exception as e:
        return f"Failed to rename file: {e}"
