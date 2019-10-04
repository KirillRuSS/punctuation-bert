import json
import os
import random

__json = json.load(open('config.json', 'r'))

DATA_DIR = __json.get('data_dir')
SENTENCE_LIMIT = __json.get('sentence_limit')
MAX_SENTENCE_LEN = __json.get('max_sentence_len')

MODEL_PATH = __json.get('model_path')
CONFIG_PATH = os.path.join(MODEL_PATH, __json.get('config_path'))
CHECKPOINT_PATH = os.path.join(MODEL_PATH, __json.get('checkpoint_path'))
VOCAB_PATH = os.path.join(MODEL_PATH, __json.get('vocab_path'))

PUNCTUATION_MARKS = __json.get('punctuation_marks')
SIGN_HIDING_PROBABILITY = __json.get('sign_hiding_probability')

random.seed(20)
