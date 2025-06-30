import os
import argparse
import shutil


def separate_files(source_dir):
    file_types = {
        'documents': ['.doc', '.docx', '.txt', '.odt'],
        'pdfs': ['.pdf'],
        'images': ['.jpg', '.jpeg', '.png', '.gif'],
        'videos': ['.mp4', '.avi', '.mov'],
        'audios': ['.mp3', '.wav', '.aac'],
        'others': []
    }

    for folder in file_types.keys():
        os.makedirs(os.path.join(source_dir, folder), exist_ok=True)

    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)

        if os.path.isdir(file_path):
            continue

        _, ext = os.path.splitext(filename)

        moved = False
        for folder, extensions in file_types.items():
            if ext.lower() in extensions:
                shutil.move(file_path, os.path.join(source_dir, folder, filename))
                moved = True
                break

        if not moved:
            shutil.move(file_path, os.path.join(source_dir, 'others', filename))


def main():
    parser = argparse.ArgumentParser(description='Separate files by type in a given directory.')
    parser.add_argument('source_dir', type=str, help='The source directory containing files to separate.')

    args = parser.parse_args()

    separate_files(args.source_dir)


if __name__ == '__main__':
    main()
