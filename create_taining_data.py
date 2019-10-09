import os

import config as cf


def get_files_paths(data_dir: str) -> list:
    files = []

    for (r, d, f) in os.walk(data_dir):
        for file in f:
            if '.txt' in file:
                files.append(os.path.join(r, file))
    return files

if __name__ == "__main__":
    files_paths = get_files_paths(cf.DATA_DIR)

    input_file = ""
    for files_path in files_paths:
        input_file += files_path + ","
        break
    print(input_file)

    output_file = "C:/Users/79105/Documents/GitHub/punctuation-bert/data/train/wiki_train"
    os.system('python create_pretraining_data.py -input_file=' + input_file + " -output_file=" + output_file)