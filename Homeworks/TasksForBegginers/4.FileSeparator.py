import os
import argparse
import shutil
from collections import defaultdict


def separate_files_by_extension(source_dir):
    try:
        extensions_seen = defaultdict(list)

        for filename in os.listdir(source_dir):
            filepath = os.path.join(source_dir, filename)

            if os.path.isdir(filepath):
                continue

            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            extensions_seen[ext].append(filename)

        for ext in extensions_seen.keys():
            if ext:
                ext_dir = os.path.join(source_dir, f"ext_{ext[1:]}")
                os.makedirs(ext_dir, exist_ok=True)

        for ext, filenames in extensions_seen.items():
            if ext:
                ext_dir = os.path.join(source_dir, f"ext_{ext[1:]}")
                for filename in filenames:
                    src = os.path.join(source_dir, filename)
                    dst = os.path.join(ext_dir, filename)
                    shutil.move(src, dst)

        if '' in extensions_seen:
            no_ext_dir = os.path.join(source_dir, "no_extension")
            os.makedirs(no_ext_dir, exist_ok=True)
            for filename in extensions_seen['']:
                src = os.path.join(source_dir, filename)
                dst = os.path.join(no_ext_dir, filename)
                shutil.move(src, dst)

    except Exception as e:
        print(f"Error occurred: {e}")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(description='Organize files by their extensions')
    parser.add_argument('source_dir', type=str, help='Directory to organize')
    args = parser.parse_args()

    if not os.path.isdir(args.source_dir):
        print(f"Error: Directory '{args.source_dir}' does not exist")
        return

    success = separate_files_by_extension(args.source_dir)
    if success:
        print(f"Files organized in '{args.source_dir}'")


if __name__ == '__main__':
    main()
