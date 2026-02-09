import sys
import os

def clear_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    try:
        # Clear the file content by opening in write mode and immediately closing (or writing empty string)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("")
        print(f"Successfully cleared {file_path}")
    except Exception as e:
        print(f"Error clearing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 clear_file.py <file_path>")
        sys.exit(1)

    clear_file(sys.argv[1])
