import os

def list_contents(path):
    all_items = os.listdir(path)
    directories = [item for item in all_items if os.path.isdir(os.path.join(path, item))]
    files = [item for item in all_items if os.path.isfile(os.path.join(path, item))]

    print("Directories:", directories)
    print("Files:", files)
    print("All contents:", all_items)

specified_path = input("Enter the path: ")
list_contents(specified_path)

