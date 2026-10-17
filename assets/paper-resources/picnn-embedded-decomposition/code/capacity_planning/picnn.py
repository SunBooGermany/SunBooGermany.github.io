"""PICNN with one convex hidden layer and a conditioning network."""
from pathlib import Path
import json
import numpy as np
import torch
from torch import nn


def input_dimensions(problem):
    c_dim = sum(len(g)-1 for g in problem.groups) + 1
    return c_dim, c_dim + 5


def state_action_input(problem, state, exog, action):
    carried = [state[i] for group in problem.groups for i in group[1:]]
    return np.asarray(carried + [exog[0]] + list(action) + list(exog[1:]), dtype=np.float64)


class PICNN(nn.Module):
    def __init__(self, c_dim, hidden=256, u_hidden=64, alpha=0.0):
        super().__init__()
        if not 0 <= alpha <= 1 or hidden < 1 or u_hidden < 1:
            raise ValueError('Invalid PICNN dimensions or activation slope')
        self.c_dim, self.hidden, self.u_hidden, self.alpha = c_dim, hidden, u_hidden, alpha
        self.U1_W = nn.Parameter(0.01 * torch.randn(u_hidden, 2))
        self.U1_b = nn.Parameter(torch.zeros(u_hidden))
        self.U2_g_W = nn.Parameter(0.01 * torch.randn(hidden, u_hidden))
        self.U2_g_b = nn.Parameter(torch.zeros(hidden))
        self.U2_Wc_W = nn.Parameter(0.01 * torch.randn(hidden*c_dim, u_hidden))
        self.U2_Wc_b = nn.Parameter(torch.zeros(hidden*c_dim))
        self.U2_Wy_W = nn.Parameter(0.01 * torch.randn(hidden*3, u_hidden))
        self.U2_Wy_b = nn.Parameter(torch.zeros(hidden*3))
        self.raw_w_out = nn.Parameter(torch.zeros(hidden))

    def forward(self, z):
        c, action, u = z[:, :self.c_dim], z[:, self.c_dim:self.c_dim+3], z[:, -2:]
        hu = torch.tanh(u @ self.U1_W.t() + self.U1_b)
        wc = (hu @ self.U2_Wc_W.t() + self.U2_Wc_b).view(-1,self.hidden,self.c_dim)
        wy = (hu @ self.U2_Wy_W.t() + self.U2_Wy_b).view(-1,self.hidden,3)
        s = hu @ self.U2_g_W.t() + self.U2_g_b
        s = s + torch.einsum('bmc,bc->bm',wc,c) + torch.einsum('bmy,by->bm',wy,action)
        return (torch.maximum(s,self.alpha*s)*torch.nn.functional.softplus(self.raw_w_out)).sum(dim=1)

    def arrays(self):
        return {name:value.detach().cpu().numpy().copy() for name,value in self.state_dict().items()}


def condition(problem, state, exog, weights, alpha=0.0):
    """Form affine preactivations in investment actions for fixed state and exogenous inputs."""
    c_dim, _ = input_dimensions(problem)
    z = state_action_input(problem,state,exog,[0.,0.,0.])
    c, u = z[:c_dim], z[-2:]
    w = {name:np.asarray(value,dtype=np.float64) for name,value in weights.items()}
    hu = np.tanh(w['U1_W'] @ u + w['U1_b'])
    wc = (w['U2_Wc_W'] @ hu + w['U2_Wc_b']).reshape(-1,c_dim)
    wy = (w['U2_Wy_W'] @ hu + w['U2_Wy_b']).reshape(-1,3)
    offset = w['U2_g_W'] @ hu + w['U2_g_b'] + wc @ c
    # Evaluate softplus in float32 to match the archived checkpoints.
    w_out = torch.nn.functional.softplus(torch.as_tensor(weights['raw_w_out'])).numpy()
    return dict(offset=offset.tolist(), Wy=wy.tolist(), w_out=w_out.tolist(), alpha=alpha, bank=[])


def save_policy(folder, problem, networks, settings, epoch):
    folder = Path(folder)
    folder.mkdir(parents=True,exist_ok=True)
    for stage,net in networks.items():
        np.savez_compressed(folder / f'stage_{stage:02d}.npz', **net.arrays())
    metadata = dict(stages=problem.T, uncertainty=problem.c['uncertainty'],
        hidden=next(iter(networks.values())).hidden,
        u_hidden=next(iter(networks.values())).u_hidden,
        alpha=next(iter(networks.values())).alpha,
        epoch_completed=epoch, settings=settings, solver='SciPy HiGHS dual simplex')
    (folder / 'policy.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')


def load_policy(folder, problem):
    folder = Path(folder)
    metadata = json.loads((folder/'policy.json').read_text(encoding='utf-8'))
    if metadata['stages'] != problem.T or abs(metadata['uncertainty']-problem.c['uncertainty'])>1e-12:
        raise ValueError('Policy and problem configurations differ')
    arrays = {}
    for stage in range(2,problem.T+1):
        with np.load(folder/f'stage_{stage:02d}.npz',allow_pickle=False) as archive:
            arrays[stage] = {key:archive[key].copy() for key in archive.files}
    return arrays, metadata
