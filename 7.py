import os
def copy_file(source, destination):
    try:
        with open(source, 'r', encoding='utf-8') as src:
            content = src.read()
        with open(destination, 'w', encoding='utf-8') as dest:
            dest.write(content)
        print(f"File copied from '{source}' to '{destination}'.")
    except FileNotFoundError:
        print("Source file not found!")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
source_file = "C://Users//ASUS//Downloads//dfg.txt"
destination_file = "C://Users//ASUS//Downloads//copy.txt"
copy_file(source_file, destination_file)
