import torch
from torch.optim.optimizer import Optimizer

class SGD_Multi_LR(Optimizer):

    def __init__(self, params, lr_init=0.005):

        LR = [lr_init*torch.ones(p.shape) for p in params]
        defaults = dict(lr=LR)
        super(SGD_Multi_LR, self).__init__(params, defaults)

    def __setstate__(self, state):
        super(SGD_Multi_LR, self).__setstate__(state)

    def step(self, closure=None):
        """Performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:
            for p, lr in zip(group['params'], group['lr']):
                if p.grad is None:
                    continue
                d_p = p.grad.data
                p_change = -lr * d_p
                p.data.add_(p_change)
        return loss