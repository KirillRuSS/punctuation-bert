from keras_bert import load_trained_model_from_checkpoint
from BERT import tokenization

import config as cf


class Model:
    def __init__(self):
        # создаем объект для перевода строки с пробелами в токены
        self.tokenizer = tokenization.FullTokenizer(vocab_file=cf.VOCAB_PATH, do_lower_case=False)

        # загружаем модель
        print('Loading model...')
        self.model = load_trained_model_from_checkpoint(cf.CONFIG_PATH, cf.CHECKPOINT_PATH, training=True)
        self.model.summary()
        print('OK')


