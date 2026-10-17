"""Train PICNN continuation values with replay and multi-successor targets."""
from collections import deque
from copy import deepcopy
from pathlib import Path
import json, math, random, time
import numpy as np
import torch
from .picnn import PICNN, condition, input_dimensions, state_action_input, save_policy, load_policy
from .policies import evaluate


DEFAULTS = dict(epochs=10000,successors=4,hidden=256,u_hidden=64,alpha=0.0,
    replay_max=100,batch_size=20,grad_steps=2,lr=1e-4,weight_decay=1e-6,
    epsilon_init=1.0,explore_std_init=1.0,explore_decay=0.9997,epsilon_decay=0.9997,
    q_ramp_epochs=10000,target_soft_tau=0.001,loss='mse',
    checkpoint_start=7500,checkpoint_every=100,validation_start=400,validation_rounds=[50,50,300])


def sample_next(problem, observed, rngs):
    return [value*min(hi,max(lo,rng.gauss(mu,sigma)))
        for value,rng,(mu,sigma,lo,hi) in zip(observed,rngs,problem.c['exog_parameters'])]


def exog_rngs(seed):
    return [random.Random(seed+offset) for offset in [1001,2002,3003]]


def explore(problem,t,state,observed,greedy,std,rng):
    greedy = np.asarray(greedy,dtype=float)
    for _ in range(20):
        noise = np.clip([rng.gauss(0.,std) for _ in range(3)],-2*std,2*std)
        candidate = np.maximum(greedy+noise,0.)
        for trial in [candidate]+[np.maximum(greedy+(candidate-greedy)*0.5**k,0.) for k in range(1,7)]:
            try:
                problem.stage(t,state,observed,fixed_action=trial,feasibility_only=True)
                return trial.tolist()
            except RuntimeError as error:
                if 'infeasible' not in str(error).lower():
                    raise
    return greedy.tolist()


def fit(net, samples, settings):
    """Fit replay samples with a newly initialized Adam optimizer."""
    if len(samples)<5:
        return None
    z = torch.tensor(np.stack([item[0] for item in samples]),dtype=torch.float32)
    target = torch.tensor([item[1] for item in samples],dtype=torch.float32)
    opt = torch.optim.Adam(net.parameters(),lr=settings['lr'],weight_decay=settings['weight_decay'])
    batch = min(settings['batch_size'],len(samples))
    if batch <= 0:
        batch = len(samples)
    permutation, pointer = None, 0
    for _ in range(settings['grad_steps']):
        if batch == len(samples):
            zb,yb = z,target
        else:
            if permutation is None or pointer+batch>len(samples):
                permutation = torch.randperm(len(samples)); pointer = 0
            indices = permutation[pointer:pointer+batch]; pointer += batch
            zb,yb = z[indices],target[indices]
        prediction = net(zb)
        loss = torch.nn.functional.mse_loss(prediction,yb)
        if not torch.isfinite(loss):
            raise RuntimeError('Nonfinite regression loss')
        opt.zero_grad(set_to_none=True); loss.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(),10.0); opt.step()
    return float(loss.detach())


def train(problem, output, seed=0, **overrides):
    settings = {**DEFAULTS,**overrides}
    if settings['loss'] != 'mse':
        raise ValueError('PICNN training supports MSE loss only')
    for name in ['epochs','successors','replay_max','grad_steps','checkpoint_every','q_ramp_epochs']:
        if settings[name] <= 0:
            raise ValueError(f'{name} must be positive')
    output = Path(output); output.mkdir(parents=True,exist_ok=True)
    if (output/'selected_policy').exists():
        raise FileExistsError('Output already contains a selected policy; use a new output directory')
    torch.set_num_threads(1); torch.manual_seed(seed)
    rng_master = random.Random(seed)
    c_dim,_ = input_dimensions(problem)
    networks = {k:PICNN(c_dim,settings['hidden'],settings['u_hidden'],settings['alpha'])
                for k in range(2,problem.T+1)}
    targets = deepcopy(networks)
    replay = {k:deque(maxlen=settings['replay_max']) for k in networks}
    history,checkpoints = [],[]
    started = time.perf_counter()
    ramp = min(settings['epochs'],settings['q_ramp_epochs'])
    for epoch in range(settings['epochs']):
        q_weight = min(1.,(epoch+1)/ramp)
        epsilon = settings['epsilon_init']*settings['epsilon_decay']**epoch
        std = settings['explore_std_init']*settings['explore_decay']**epoch
        online = {k:net.arrays() for k,net in networks.items()}
        frozen = {k:net.arrays() for k,net in targets.items()}
        roll_seed = rng_master.randint(0,2**31-1)
        action_rng = random.Random(roll_seed+11)
        rngs = [random.Random(roll_seed+offset) for offset in [101,202,303]]
        state,observed,pending,total = problem.initial[:],problem.exog0[:],None,0.
        for t in range(problem.T):
            payload = condition(problem,state,observed,online[t+2],settings['alpha']) if t<problem.T-1 else None
            target_payload = condition(problem,state,observed,frozen[t+2],settings['alpha']) if t<problem.T-1 else None
            greedy = problem.stage(t,state,observed,picnn=payload,q_alpha=q_weight)
            target = problem.stage(t,state,observed,picnn=target_payload,q_alpha=q_weight)['objective']
            if pending is not None:
                previous_z,base_state,parent = pending
                values = [target]
                child_rngs = exog_rngs(seed*10_000_000+epoch*100_000+(t+1))
                for _ in range(settings['successors']-1):
                    child = sample_next(problem,parent,child_rngs)
                    child_payload = condition(problem,base_state,child,frozen[t+2],settings['alpha']) if t<problem.T-1 else None
                    values.append(problem.stage(t,base_state,child,picnn=child_payload,q_alpha=q_weight)['objective'])
                # Average terminal-stage targets over the sampled successors.
                replay[t+1].append((previous_z,float(np.mean(values))))
            action = greedy['action']
            if action_rng.random()<epsilon and std>0:
                action = explore(problem,t,state,observed,action,std,action_rng)
            if np.allclose(action,greedy['action'],atol=1e-12,rtol=0.):
                immediate = greedy['immediate']
            else:
                immediate = problem.stage(t,state,observed,fixed_action=action)['immediate']
            total += problem.gamma**t*immediate
            nxt = problem.next_y(state,action)
            if t<problem.T-1:
                pending = (state_action_input(problem,state,observed,action),nxt,observed[:])
            state,observed = nxt,sample_next(problem,observed,rngs)
        losses = {k:fit(net,list(replay[k]),settings) for k,net in networks.items()}
        with torch.no_grad():
            for k,net in networks.items():
                for target,param in zip(targets[k].parameters(),net.parameters()):
                    target.mul_(1-settings['target_soft_tau']).add_(param,alpha=settings['target_soft_tau'])
        history.append(dict(epoch=epoch+1,training_path_NPC=total,loss=losses,q_weight=q_weight))
        if (epoch+1)>=settings['checkpoint_start'] and (epoch+1)%settings['checkpoint_every']==0:
            folder = output/'checkpoints'/f'epoch_{epoch+1:05d}'
            save_policy(folder,problem,networks,settings,epoch+1); checkpoints.append(folder)
        if (epoch+1)%100==0 or epoch==0:
            print(f'PICNN epoch {epoch+1}/{settings["epochs"]}, successors={settings["successors"]}, elapsed={time.perf_counter()-started:.1f}s',flush=True)
    final = output/'checkpoints'/f'epoch_{settings["epochs"]:05d}'
    if final not in checkpoints:
        save_policy(final,problem,networks,settings,settings['epochs']); checkpoints.append(final)
    (output/'training_history.json').write_text(json.dumps(history,indent=2),encoding='utf-8')
    (output/'training_settings.json').write_text(json.dumps(dict(training_seed=seed,**settings),indent=2),encoding='utf-8')
    winner = select_checkpoint(problem,checkpoints,settings,output)
    import shutil
    shutil.copytree(winner,output/'selected_policy')
    return output/'selected_policy'


def select_checkpoint(problem, checkpoints, settings, output):
    """Select a checkpoint in three disjoint validation rounds (default: 50/50/300 paths)."""
    counts = settings['validation_rounds']
    if len(counts)!=3 or any(n<1 for n in counts) or settings['validation_start']<400:
        raise ValueError('Use three positive validation rounds on seeds starting at >=400')
    scores = {str(folder):[] for folder in checkpoints}
    active = list(checkpoints); start = settings['validation_start']; round_records=[]
    for index,count in enumerate(counts):
        for folder in active:
            arrays,meta = load_policy(folder,problem)
            _,rows = evaluate(problem,range(start,start+count),'proposed',picnn=arrays,alpha=meta['alpha'])
            scores[str(folder)].extend(row['NPC'] for row in rows)
        active.sort(key=lambda path:(float(np.mean(scores[str(path)])),str(path)))
        round_records.append(dict(round=index+1,seed_start=start,paths=count,
            rankings=[dict(checkpoint=path.name,mean_NPC=float(np.mean(scores[str(path)]))) for path in active]))
        if index==0:
            active = active[:min(len(active),math.isqrt(len(checkpoints))+1)]
        elif index==1:
            active = active[:min(2,len(active))]
        start += count
    (Path(output)/'validation_selection.json').write_text(json.dumps(round_records,indent=2),encoding='utf-8')
    return active[0]
