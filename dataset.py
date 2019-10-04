import os
import numpy as np
from copy import copy
from tensorflow.contrib.learn.python.learn.estimators._sklearn import train_test_split

import config as cf
from utils import tokenization
from utils.utils import strip_accents, is_mark_known


class Dataset:

    def __init__(self):
        self.data_dir = cf.DATA_DIR
        self.tokenizer = tokenization.FullTokenizer(vocab_file=cf.VOCAB_PATH, do_lower_case=False)

        input_ids, output_ids, attention_masks = self.load_data(self.data_dir)
        self.train_inputs, self.validation_inputs, \
        self.train_outputs, self.validation_outputs, \
        self.train_masks, self.validation_masks = self.data_postprocessing(input_ids, output_ids, attention_masks)

    def load_data(self, data_dir: str) -> (np.array, np.array, np.array):
        files_paths = self.get_files_paths(data_dir)

        input_ids = []
        output_ids = []
        attention_masks = []
        for path in files_paths:
            f = open(path, encoding='utf-8')
            for line in f:
                line = line.replace('\n', '')

                if len(line.split(' ')) <= 1 or line[1] == '<':
                    continue

                input_id, output_id, attention_mask = self.sentence_postprocessing(line)

                input_ids.append(input_id)
                output_ids.append(output_id)
                attention_masks.append(attention_mask)

                if len(input_ids) >= cf.SENTENCE_LIMIT:
                    break
            if len(input_ids) >= cf.SENTENCE_LIMIT:
                break
        print("Загруженно {} предложений".format(len(input_ids)))

        input_ids = np.array(input_ids)
        attention_masks = np.array(attention_masks)
        output_ids = np.array(output_ids)

        return input_ids, output_ids, attention_masks

    def get_files_paths(self, data_dir: str) -> list:
        files = []

        for (r, d, f) in os.walk(data_dir):
            for file in f:
                if '.txt' in file:
                    files.append(os.path.join(r, file))
        return files

    def sentence_postprocessing(self, sentence: str) -> (list, list, list):
        sentence = strip_accents(sentence)

        sentence = sentence.replace('(', '')
        sentence = sentence.replace(')', '')
        sentence = sentence.replace(',', ' , ')
        sentence = sentence.replace(':', ' : ')
        sentence = sentence.replace('  ', ' ')

        # Преобразование в токены
        sentence = sentence.split(' ')
        tokens = ['[CLS]']
        for i in range(len(sentence)):
            tokens = tokens + self.tokenizer.tokenize(sentence[i])
        tokens = tokens + ['[SEP]']

        # Преобразование в массив индексов
        output_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        output_ids = output_ids + [0] * (cf.MAX_SENTENCE_LEN - len(output_ids))
        output_ids = output_ids[:512]

        # Добавление маски
        input_ids, attention_masks = self.get_attention_masks(output_ids)

        return input_ids, output_ids, attention_masks

    def get_attention_masks(self, output_ids: list) -> (list, list):
        attention_masks = [0] * cf.MAX_SENTENCE_LEN

        input_ids = copy(output_ids)
        for i in range(len(input_ids)):
            if not is_mark_known(input_ids[i]):
                attention_masks[i] = 0.0

                # Заменяем символ на маску
                input_ids[i] = 103
            else:
                attention_masks[i] = 1.0

        return input_ids, attention_masks

    def data_postprocessing(self, input_ids: np.array, output_ids: np.array, attention_masks: np.array):
        train_inputs, validation_inputs, train_outputs, validation_outputs = train_test_split(input_ids, output_ids,
                                                                                              random_state=42, test_size=0.1)
        train_masks, validation_masks, _, _ = train_test_split(attention_masks, input_ids,
                                                               random_state=42, test_size=0.1)
        return train_inputs, validation_inputs, train_outputs, validation_outputs, train_masks, validation_masks
