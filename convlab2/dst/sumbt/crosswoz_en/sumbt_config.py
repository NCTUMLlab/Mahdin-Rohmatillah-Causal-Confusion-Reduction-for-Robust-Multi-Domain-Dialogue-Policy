import os
import convlab2
class DotMap():
    def __init__(self):
        self.max_label_length = 35
        self.num_rnn_layers = 1
        self.zero_init_rnn = False
        self.attn_head = 4
        self.do_eval = True
        self.do_train = False
        self.train_batch_size = 3
        self.dev_batch_size = 1
        self.eval_batch_size  = 16
        self.learning_rate = 5e-5
        self.warmup_proportion = 0.1
        self.local_rank = -1
        self.seed = 42
        self.gradient_accumulation_steps = 1
        self.fp16 = False
        self.loss_scale = 0
        self.do_not_use_tensorboard = False
        self.fix_utterance_encoder = False
        self.do_eval = True
        self.num_train_epochs = 300

        self.bert_model = os.path.join(convlab2.get_root_path(), "pre-trained-models/bert-base-uncased")
        self.bert_model_cache_dir = os.path.join(convlab2.get_root_path(), "pre-trained-models/")
        self.bert_model_name = "bert-base-uncased"
        self.do_lower_case = True
        self.task_name = 'bert-gru-sumbt'
        self.nbt = 'rnn'
        self.target_slot = 'all'
        self.distance_metric = 'euclidean'
        self.patience = 15

        self.hidden_dim = 300
        self.max_seq_length = 35
        self.max_turn_length = 23

        self.fp16_loss_scale = 0.0
        self.data_dir = 'data/crosswoz_en/'
        self.tf_dir = 'tensorboard'
        self.tmp_data_dir = 'processed_data/'
        self.output_dir = 'model_output/'

args = DotMap()