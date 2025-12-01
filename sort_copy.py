# sort_copy.py
import argparse
import os
import shutil
import sys

def parse_args():
    p = argparse.ArgumentParser(description="Recursively copy files from source to destination and sort into subdirs by extension.")
    p.add_argument("src", help="Path to source directory")
    p.add_argument("dest", nargs="?", default="dist", help="Path to destination directory (default: dist)")
    return p.parse_args()

def safe_makedirs(path):
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory {path}: {e}", file=sys.stderr)
        raise

def unique_path(path):
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    i = 1
    while True:
        candidate = f"{base}({i}){ext}"
        if not os.path.exists(candidate):
            return candidate
        i += 1

def copy_file_to_ext_dir(file_path, src_root, dest_root):
    try:
        rel = os.path.relpath(file_path, src_root)
    except Exception:
        rel = os.path.basename(file_path)
    _, ext = os.path.splitext(file_path)
    ext_name = ext.lstrip(".").lower() if ext else "no_extension"
    dest_dir = os.path.join(dest_root, ext_name)
    safe_makedirs(dest_dir)
    dest_file = os.path.join(dest_dir, os.path.basename(file_path))
    dest_file = unique_path(dest_file)
    try:
        shutil.copy2(file_path, dest_file)
    except (PermissionError, OSError) as e:
        print(f"Failed to copy {file_path} -> {dest_file}: {e}", file=sys.stderr)
        return False
    return True

def traverse_and_copy(path, src_root, dest_root):
    try:
        for entry in os.listdir(path):
            full = os.path.join(path, entry)
            
            try:
                if os.path.commonpath([os.path.abspath(full), os.path.abspath(dest_root)]) == os.path.abspath(dest_root):
                    
                    continue
            except Exception:
                pass
            try:
                if os.path.islink(full):
                   
                    continue
                if os.path.isdir(full):
                    traverse_and_copy(full, src_root, dest_root)
                elif os.path.isfile(full):
                    copy_file_to_ext_dir(full, src_root, dest_root)
            except PermissionError as e:
                print(f"Permission denied accessing {full}: {e}", file=sys.stderr)
            except OSError as e:
                print(f"OS error accessing {full}: {e}", file=sys.stderr)
    except PermissionError as e:
        print(f"Permission denied reading directory {path}: {e}", file=sys.stderr)
    except FileNotFoundError as e:
        print(f"Directory not found {path}: {e}", file=sys.stderr)
    except OSError as e:
        print(f"OS error listing directory {path}: {e}", file=sys.stderr)

def main():
    args = parse_args()
    src = os.path.abspath(args.src)
    dest = os.path.abspath(args.dest)

    if not os.path.exists(src):
        print(f"Source directory does not exist: {src}", file=sys.stderr)
        sys.exit(2)
    if not os.path.isdir(src):
        print(f"Source is not a directory: {src}", file=sys.stderr)
        sys.exit(2)

    
    try:
        if os.path.commonpath([src, dest]) == dest:
            print("Destination directory is inside the source directory. Choose a different destination to avoid recursion.", file=sys.stderr)
            sys.exit(2)
    except Exception:
        pass

    safe_makedirs(dest)
    traverse_and_copy(src, src, dest)
    print("Done.")

if __name__ == "__main__":
    main()


   

