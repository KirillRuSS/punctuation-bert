import json
import os
import random

__json = json.load(open('config.json', 'r'))

DATA_DIR = __json.get('data_dir')

PUNCTUATION_TOKEN = __json.get('punctuation_token')
MASKED_TOKEN = __json.get('masked_token')
MAIN_DIRECTORY = __json.get('main_directory')

random.seed(42)
