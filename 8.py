import os

def delete_file(file_path):
    if os.path.exists(file_path):
        if os.access(file_path, os.W_OK):  # Check if writable
            os.remove(file_path)
            print(f"File '{file_path}' deleted successfully.")
        else:
            print("No permission to delete the file.")
    else:
        print("File not found!")

# Example usage
file_path = "C:\\Users\\ASUS\\Desktop\\output.txt"
delete_file(file_path)
