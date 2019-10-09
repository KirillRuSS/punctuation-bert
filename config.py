import json
import os
import random

__json = json.load(open('config.json', 'r'))

DATA_DIR = __json.get('data_dir')

PUNCTUATION_TOKEN = __json.get('punctuation_token')
MASKED_TOKEN = __json.get('masked_token')
MAIN_DIRECTORY = __json.get('main_directory')


bert_config_file = __json.get('bert_config_file')
input_file = __json.get('input_file')
output_dir = __json.get('output_dir')
init_checkpoint = __json.get('init_checkpoint')
do_train = __json.get('do_train')
do_eval = __json.get('do_eval')

random.seed(42)
