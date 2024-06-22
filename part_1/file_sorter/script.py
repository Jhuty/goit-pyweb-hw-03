import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_file(file_path, target_dir):
    ext = os.path.splitext(file_path)[1].lower().strip('.')
    if not ext:
        return
    ext_dir = os.path.join(target_dir, ext)
    os.makedirs(ext_dir, exist_ok=True)
    shutil.copy2(file_path, ext_dir)

def process_directory(directory, target_dir, executor):
    for root, dirs, files in os.walk(directory):
        futures = []
        for file in files:
            file_path = os.path.join(root, file)
            futures.append(executor.submit(process_file, file_path, target_dir))
        for future in as_completed(futures):
            future.result()

def main(source_dir, target_dir):
    with ThreadPoolExecutor() as executor:
        process_directory(source_dir, target_dir, executor)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <source_dir> [target_dir]")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    target_dir = sys.argv[2] if len(sys.argv) > 2 else 'dist'
    
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        sys.exit(1)
    
    os.makedirs(target_dir, exist_ok=True)
    
    main(source_dir, target_dir)
