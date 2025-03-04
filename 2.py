import os

def check_path_access(path):
    exists = os.path.exists(path)
    readable = os.access(path, os.R_OK)  
    writable = os.access(path, os.W_OK)  
    executable = os.access(path, os.X_OK)  

    print(f"Path: {path}")
    print(f"Exists: {'Yes' if exists else 'No'}")
    print(f"Readable: {'Yes' if readable else 'No'}")
    print(f"Writable: {'Yes' if writable else 'No'}")
    print(f"Executable: {'Yes' if executable else 'No'}")

specified_path = input("Enter the path: ")
check_path_access(specified_path)
