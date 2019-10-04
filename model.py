from keras_bert import load_trained_model_from_checkpoint
from utils import tokenization



folder = "multi_cased_L-12_H-768_A-12"

config_path = folder+'/bert_config.json'
checkpoint_path = folder+'/bert_model.ckpt'
vocab_path = folder+'/vocab.txt'

# создаем объект для перевода строки с пробелами в токены
tokenizer = tokenization.FullTokenizer(vocab_file=vocab_path, do_lower_case=False)

# загружаем модель
print('Loading model...')
model = load_trained_model_from_checkpoint(config_path, checkpoint_path, training=True)
model.summary()          # информация о слоях нейросети - количество параметров и т.д.
print('OK')


