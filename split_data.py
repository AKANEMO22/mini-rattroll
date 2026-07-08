import os
import glob

def split_file(filepath, chunk_size=90 * 1024 * 1024):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return
        
    file_size = os.path.getsize(filepath)
    if file_size <= chunk_size:
        print(f"File {filepath} is smaller than chunk size, no need to split.")
        return
        
    part_num = 0
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            part_filepath = f"{filepath}.part{part_num:03d}"
            with open(part_filepath, 'wb') as part_f:
                part_f.write(chunk)
            print(f"Created {part_filepath}")
            part_num += 1

if __name__ == "__main__":
    csv_files = glob.glob('data/**/*.csv', recursive=True)
    for csv_file in csv_files:
        if os.path.getsize(csv_file) > 90 * 1024 * 1024:
            print(f"Splitting {csv_file}...")
            split_file(csv_file)
            print(f"Done splitting {csv_file}")
