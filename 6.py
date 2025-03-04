import os
import string

def generate_text_files():
    for letter in string.ascii_uppercase:  # A-Z
        file_name = f"{letter}.txt"
        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(f"This is file {file_name}\n")
            print(f"Created: {file_name}")
        except Exception as e:
            print(f"Error: {e}")

# Run the function
generate_text_files()
