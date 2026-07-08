import os
import glob

def join_file(filepath):
    parts = sorted(glob.glob(f"{filepath}.part*"))
    if not parts:
        print(f"No parts found for {filepath}")
        return
        
    print(f"Joining {len(parts)} parts for {filepath}...")
    with open(filepath, 'wb') as out_f:
        for part in parts:
            with open(part, 'rb') as in_f:
                out_f.write(in_f.read())
            print(f"Appended {part}")

if __name__ == "__main__":
    # Find all base files by looking at .part000
    first_parts = glob.glob('data/**/*.part000', recursive=True)
    for first_part in first_parts:
        base_filepath = first_part.replace('.part000', '')
        if not os.path.exists(base_filepath):
            join_file(base_filepath)
        else:
            print(f"File {base_filepath} already exists, skipping...")
