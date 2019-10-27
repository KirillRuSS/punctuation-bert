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


input_file = "data/voina-i-mir.fb2"
output_file = "data/train"
max_text_size = 1000 * 1000 * 1

input = open(input_file, 'r', encoding="utf-8")

text = ""
text_id = 0
output = open(os.path.join(output_file, str(text_id) + ".txt"), 'w', encoding="utf-8")
for line in input:
    if sys.getsizeof(text) > max_text_size:
        text, text_id, output = GoToNextFile(text, text_id, output)

    line = re.sub(r'[^А-Яа-я ,.!?:]', '', line)
    if len(re.sub(r'[^А-Яа-я]', '', line)) == 0:
        continue

    line = re.sub('[,.!?:] *[,.!?:]', ' ', line)
    line = re.sub(' +', ' ', line)

    text += line

text, text_id, output = GoToNextFile(text, text_id, output)