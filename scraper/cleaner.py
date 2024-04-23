import os
import multiprocessing
from bs4 import BeautifulSoup
import chardet

def get_unique_filename(output_file_path, output_dir):
    filename = os.path.basename(output_file_path)
    new_filename = os.path.join(output_dir, filename)
    counter = 1
    while os.path.exists(new_filename):
        new_filename = os.path.join(output_dir, filename.replace(".html", f"_{counter}.html"))
        counter += 1
    return new_filename

def clean_file(file_path, output_dir):
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            encoding = chardet.detect(raw_data)['encoding']

        with open(file_path, 'r', encoding=encoding) as file:
            file_content = file.read()

        soup = BeautifulSoup(file_content, features="lxml")
        output_file_path = get_unique_filename(file_path, output_dir)

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

    except Exception as e:
        print(f"Error processing file in cleaner {file_path}: {e}")

def process_directory_parallel(dir_path, output_dir):
    files = [os.path.join(root, f) for root, _, fs in os.walk(dir_path, topdown=False) for f in fs if f.endswith('.html')]
    with multiprocessing.Pool() as pool:
        args = [(file, output_dir) for file in files]
        pool.starmap(clean_file, args)

if __name__ == "__main__":
    dir_path = "websites"
    output_dir = "cleaned_websites"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    process_directory_parallel(dir_path, output_dir)
