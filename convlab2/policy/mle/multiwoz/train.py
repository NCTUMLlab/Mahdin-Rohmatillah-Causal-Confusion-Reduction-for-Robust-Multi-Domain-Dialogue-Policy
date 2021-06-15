import os
import torch
import logging
import json
import sys
from torch import nn
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(root_dir)

from convlab2.policy.rlmodule import MultiDiscretePolicy
from convlab2.policy.vector.vector_multiwoz import MultiWozVector
from convlab2.policy.mle.train import MLE_Trainer_Abstract
from convlab2.policy.mle.multiwoz.loader import ActMLEPolicyDataLoaderMultiWoz
from convlab2.util.train_util import init_logging_handler
#%%
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def weights_init(m):
    if isinstance(m, nn.Linear):
        torch.nn.init.xavier_uniform_(m.weight)
        #torch.nn.init.xavier_uniform_(m.bias)

class MLE_Trainer(MLE_Trainer_Abstract):
    def __init__(self, manager, cfg):
        self._init_data(manager, cfg)
        voc_file = os.path.join(root_dir, 'data/multiwoz/sys_da_voc.txt')
        voc_opp_file = os.path.join(root_dir, 'data/multiwoz/usr_da_voc.txt')
        vector = MultiWozVector(voc_file, voc_opp_file)
        # override the loss defined in the MLE_Trainer_Abstract to support pos_weight
        pos_weight = 5 * torch.ones(vector.da_dim).to(device=DEVICE)
        pos_weight1 = 5 * torch.ones(24).to(device=DEVICE)
        pos_weight2 = 8 * torch.ones(78).to(device=DEVICE)
        self.multi_entropy_loss = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
        self.multi_entropy_loss1 = nn.BCEWithLogitsLoss(pos_weight=pos_weight1)
        self.multi_entropy_loss2 = nn.BCEWithLogitsLoss(pos_weight=pos_weight2)
        self.policy = MultiDiscretePolicy(vector.state_dim, cfg['h_dim'], vector.da_dim).to(device=DEVICE)
        #self.policy.apply(weights_init)
        self.policy.eval()
        self.policy_optim = torch.optim.AdamW(self.policy.parameters())

if __name__ == '__main__':
    manager = ActMLEPolicyDataLoaderMultiWoz()
    with open('config.json', 'r') as f:
        cfg = json.load(f)
    init_logging_handler(cfg['log_dir'])
    agent = MLE_Trainer(manager, cfg)
    
    logging.debug('start training')
     
    best = float('inf')
    for e in range(20):
        agent.imitating(e)
        best = agent.imit_test(e, best)
        print(best)
