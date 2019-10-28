import os
import time
import timeit
import string
import config as cf
from threading import Thread


def get_files_paths(data_dir: str) -> list:
    files = []

    for (r, d, f) in os.walk(data_dir):
        for file in f:
            if '.txt' in file:
                files.append(os.path.join(r, file))
    return files


def run_create_pretraining_data(files_path, output_file, index):
    os.system('python create_pretraining_data.py -input_file=' + files_path + " -output_file=" + output_file + str(index))


if __name__ == "__main__":

    output_file = "/home/kirill/punctuation-bert/data/train/text_"
    input_file = "/home/kirill/DataSets/texts/"
    threads_number = 6

    index = 0
    start = timeit.default_timer()
    while index < 60:
        threads = []

        for i in range(threads_number):
            files_path = input_file + str(i) + '.txt'
            threads.append(Thread(target=run_create_pretraining_data, args=(files_path, output_file, index)))
            threads[-1].start()
            index += 1

            print(files_path)
            time.sleep(15)

        for i in range(threads_number):
            threads[i].join()

        stop = timeit.default_timer()
        print('Time: ', stop - start)
        start = stop
        print(index)


"""
    for i in string.ascii_uppercase:
        files_paths = get_files_paths(cf.DATA_DIR + i)

        input_file = ""
        for files_path in files_paths:
            input_file += files_path + ","

        print(input_file)

        output_file = "C:/Users/79105/Documents/GitHub/punctuation-bert/data/train/wiki_train_B" + i
        os.system('python create_pretraining_data.py -input_file=' + input_file + " -output_file=" + output_file)
"""
