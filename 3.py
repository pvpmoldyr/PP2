import os

def check_path(path):
    if os.path.exists(path):
        print("The given path exists.")
        directory = os.path.dirname(path)
        filename = os.path.basename(path)
        print(f"Directory: {directory}")
        print(f"Filename: {filename}")
    else:
        print("The given path does not exist.")

# Example usage
path = input("Enter the path: ")
check_path(path)
