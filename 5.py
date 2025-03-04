import os
def write_list_to_file(file_path, data_list):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for item in data_list:
                file.write(f"{item}\n")
        print(f"List written to '{file_path}' successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
file_path = "C:\\Users\\ASUS\\Desktop\\output.txt"
data_list = ["Apple", "Banana", "Cherry"]
write_list_to_file(file_path, data_list)
