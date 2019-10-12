import glob
import os
import re
import time
from threading import Thread


def train(main_directory: str,
          bert_config_file: str,
          input_file: list,
          output_dir: str,
          init_checkpoint: str,
          train_batch_size: int,
          num_train_steps: int,
          num_warmup_steps: int,
          save_checkpoints_steps: int):
    import run_pretraining
    run_pretraining.run(main_directory=main_directory,
                        bert_config_file=bert_config_file,
                        input_file=input_file,
                        output_dir=output_dir,
                        init_checkpoint=init_checkpoint,
                        do_train=True,
                        do_eval=True,
                        train_batch_size=train_batch_size,
                        num_train_steps=num_train_steps,
                        num_warmup_steps=num_warmup_steps,
                        save_checkpoints_steps=save_checkpoints_steps)


def validate(main_directory: str,
             bert_config_file: str,
             input_files: list,
             output_dir: str,
             evaluate_result_dir: str,
             init_checkpoint: str,
             eval_batch_size: int):
    import run_pretraining

    step = 0
    global_step = 0

    import tensorflow as tf
    writer = tf.summary.FileWriter(os.path.join(main_directory, output_dir))

    while True:
        time.sleep(1)

        files_list = glob.glob(os.path.join(main_directory, init_checkpoint) + '/*.index')
        pattern = re.compile('\d+')
        for file in files_list:
            if global_step < int(pattern.findall(file)[-1]):
                global_step = int(pattern.findall(file)[-1])

        # Если появилсь новая модель, то тестируем её
        if global_step > step:
            time.sleep(30)
            step = global_step

            for input_file in input_files:
                evaluate_result = {}

                test_thread = Thread(target=run_pretraining.run, args=(main_directory,
                                                                       bert_config_file,
                                                                       input_file,
                                                                       output_dir,
                                                                       init_checkpoint,
                                                                       False,
                                                                       True,
                                                                       None,  # train_batch_size
                                                                       eval_batch_size,
                                                                       None,  # num_train_steps
                                                                       None,  # num_warmup_steps
                                                                       None,  # save_checkpoints_steps
                                                                       evaluate_result))

                test_thread.start()
                while test_thread.is_alive():
                    time.sleep(1)

                evaluate_result_file = os.path.join(main_directory, evaluate_result_dir, "evaluate_results.txt")

                # Проверяем наличие файла, для записи результатов
                if not os.path.isfile(evaluate_result_file):
                    with open(evaluate_result_file, "w") as file:
                        for key in sorted(evaluate_result.keys()):
                            file.write("%s\t" % key)
                        file.write("\n")

                with open(evaluate_result_file, "a") as file:
                    for key in sorted(evaluate_result.keys()):
                        file.write("%.3f\t" % evaluate_result[key])
                        tf.summary.scalar(key + "_" + os.path.basename(input_file), evaluate_result[key])
                        writer.flush()
                    file.write("\t")

            with open(evaluate_result_file, "a") as file:
                file.write("\n")


def run(main_directory: str,
        bert_config_file: str,
        input_file: list,
        validation_file: list,
        output_dir: str,
        evaluate_result_dir: str,
        init_checkpoint: str,
        train_batch_size: int,
        eval_batch_size: int,
        num_train_steps: int,
        num_warmup_steps: int,
        save_checkpoints_steps: int):
    train_thread = Thread(target=train, args=(main_directory,
                                              bert_config_file,
                                              input_file,
                                              output_dir,
                                              init_checkpoint,
                                              train_batch_size,
                                              num_train_steps,
                                              num_warmup_steps,
                                              save_checkpoints_steps))

    validation_thread = Thread(target=validate, args=(main_directory,
                                                      bert_config_file,
                                                      validation_file,
                                                      output_dir,
                                                      evaluate_result_dir,
                                                      output_dir,
                                                      eval_batch_size))

    train_thread.start()
    validation_thread.start()
    train_thread.join()
    validation_thread.join()


"""
run(main_directory="C:/Users/79105/Documents/GitHub/punctuation-bert/",
    bert_config_file="multi_cased_L-12_H-768_A-12/bert_config.json",
    input_file=["data/train/wiki_train_AA"],
    validation_file=["data/test/wiki_test"],
    output_dir="data/punctuation_model",
    evaluate_result_dir="data/punctuation_model",
    init_checkpoint="multi_cased_L-12_H-768_A-12/bert_model.ckpt",
    train_batch_size=1,
    eval_batch_size=1,
    num_train_steps=2,
    num_warmup_steps=1,
    save_checkpoints_steps=1)
"""
import string
input_file = []
for l in string.ascii_uppercase:
    input_file.append("data/train/wiki/wiki_train_A" + l)
    input_file.append("data/train/wiki/wiki_train_B" + l)


run(main_directory="/content/",
    bert_config_file="pm_2000/bert_config.json",
    input_file=input_file,
    validation_file=["data/test/wiki_test", "data/test/wiki_test_p", "data/test/wiki_test_s"],
    output_dir="data/punctuation_model",
    evaluate_result_dir="data/punctuation_model",
    init_checkpoint="pm_2000/model.ckpt-35000",
    train_batch_size=12,
    eval_batch_size=4,
    num_train_steps=100000,
    num_warmup_steps=1000,
    save_checkpoints_steps=500)
