import os
def count_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            print(f"Number of lines in '{file_path}': {len(lines)}")
    except FileNotFoundError:
        print("File not found!")
    except Exception as e:
        print(f"Error: {e}")

file_path =  "C://Users//ASUS//Downloads//dfg.txt"
count_lines(file_path)
