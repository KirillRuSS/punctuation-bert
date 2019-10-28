import os
import re
import sys
from nltk.tokenize import sent_tokenize


def GoToNextFile(text, text_id, output):
    sentences = sent_tokenize(text)
    text = ""
    for sentence in sentences:
        text += sentence + '\n'

    output.write(text)
    output.close()

    text = ""
    text_id += 1
    output = open(os.path.join(output_file, str(text_id) + ".txt"), 'w', encoding="utf-8")

    return text, text_id, output


input_file = "/home/kirill/DataSets/librusec_fb2.plain"
output_file = "/home/kirill/DataSets/texts/"
max_text_size = 1024 * 1024 * 100

input = open(input_file, 'r', encoding="utf-8")

text = ""
text_id = 0
output = open(os.path.join(output_file, str(text_id) + ".txt"), 'w', encoding="utf-8")
for line in input:
    if sys.getsizeof(text) > max_text_size:
        print(text_id, sys.getsizeof(text))
        text, text_id, output = GoToNextFile(text, text_id, output)
        if text_id >= 200:
            break

    line = re.sub(r'[^А-Яа-я ,.!?:]', '', line)
    if len(re.sub(r'[^А-Яа-я]', '', line)) == 0:
        continue

    line = re.sub('[,.!?:] *[,.!?:]', ' ', line)
    line = re.sub(' +', ' ', line)

    text += line

text, text_id, output = GoToNextFile(text, text_id, output)