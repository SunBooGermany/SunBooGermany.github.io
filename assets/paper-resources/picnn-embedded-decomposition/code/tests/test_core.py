"""Numerical checks for the paper model, dual cuts, and PICNN LP embedding."""
from copy import deepcopy
from pathlib import Path
import json, tempfile, unittest
import numpy as np
import torch
from capacity_planning.config import make_config
from capacity_planning.lp import LP
from capacity_planning.model import Problem
from capacity_planning.nodes import MarkovGrid
from capacity_planning.picnn import PICNN, condition, input_dimensions, load_policy, state_action_input
from capacity_planning.policies import rollout
from capacity_planning.sddp import SDDP
from capacity_planning.training import DEFAULTS, fit, train

ROOT = Path(__file__).resolve().parent.parent


class ModelTests(unittest.TestCase):
    def test_cached_paths_match_all_original_evaluation_paths(self):
        for t in [6,24]:
            for std in [10,30]:
                p = Problem(make_config(t,std/100))
                with np.load(ROOT/f'data/source_paths_T{t}_std{std}.npz') as archive:
                    expected = archive['paths']
                np.testing.assert_allclose(np.asarray([p.path(i) for i in range(400)]),expected,rtol=1e-14,atol=1e-14)
                self.assertEqual(p.H,144)
                self.assertEqual(sum(len(g) for g in p.groups),p.n)

    def test_highs_rhs_dual_sign(self):
        lp = LP(); x = lp.var('x',cost=3.)
        lp.row({x:-1.},-2.)
        result = lp.solve()
        self.assertAlmostEqual(result['objective'],6.,places=9)
        self.assertAlmostEqual(result['dual'][0],-3.,places=9)

    def test_perfect_information_lower_than_implementable_policy(self):
        for stages,std,seed in [(6,.1,42),(6,.3,399),(24,.1,0),(24,.3,42)]:
            p = Problem(make_config(stages,std))
            perfect,_ = rollout(p,seed,'omniscient')
            myopic,_ = rollout(p,seed,'myopic')
            rh,_ = rollout(p,seed,'rh')
            self.assertLessEqual(perfect,myopic+1e-7)
            self.assertLessEqual(perfect,rh+1e-7)

    def test_vintage_capacity_and_fixed_action_accounting(self):
        p = Problem(make_config())
        result = p.stage(0,p.initial,p.exog0)
        replay = p.stage(0,p.initial,p.exog0,fixed_action=result['action'])
        self.assertAlmostEqual(replay['immediate'],result['immediate'],places=8)
        nxt = p.next_y(p.initial,result['action'])
        for group,action in zip(p.groups,result['action']):
            self.assertAlmostEqual(nxt[group[-1]],action,places=10)

    def test_sddp_matches_exact_two_stage_tree_and_valid_cuts(self):
        for nodes in [8,27]:
            p = Problem(make_config())
            grid = MarkovGrid(p,nodes)
            self.assertTrue(all(abs(sum(row)-1)<1e-12 for matrix in grid.transitions for row in matrix))
            p.T = 2
            data = grid.dump()
            data['axis_levels'],data['centres'],data['transitions'] = data['axis_levels'][:2],data['centres'][:2],data['transitions'][:1]
            tiny = MarkovGrid.from_dict(data)
            alg = SDDP(p,tiny,seed=17); alg.train(20)
            self.assertAlmostEqual(alg.history[-1]['graph_lower_bound'],p.exact_two_stage(tiny),places=5)
            state = p.next_y(p.initial,[.2,.4,.6])
            for j in range(nodes):
                exact = p.stage(1,state,tiny.centres[1][j])['objective']
                for intercept,slope in alg.cuts[1][j]:
                    self.assertLessEqual(intercept+np.dot(slope,state),exact+1e-6)

    def test_picnn_forward_equals_fixed_action_epigraph(self):
        torch.manual_seed(173)
        for stages in [6,24]:
            p = Problem(make_config(stages))
            c_dim,_ = input_dimensions(p)
            net = PICNN(c_dim,hidden=32,u_hidden=16)
            observed = p.path(42)[0]
            action = p.stage(0,p.initial,observed)['action']
            payload = condition(p,p.initial,observed,net.arrays())
            lp = p.stage(0,p.initial,observed,picnn=payload,fixed_action=action)
            z = state_action_input(p,p.initial,observed,action)
            with torch.no_grad():
                value = float(net(torch.tensor(z[None,:],dtype=torch.float32)))
            self.assertAlmostEqual(lp['q_next_value'],max(0.,value),delta=2e-6)

    def test_training_checkpoint_reload_and_terminal_successor_targets(self):
        p = Problem(make_config())
        temporary_root = ROOT/'outputs'/'test_temporary_files'
        temporary_root.mkdir(parents=True,exist_ok=True)
        for successors in [4,16]:
            with tempfile.TemporaryDirectory(dir=temporary_root) as directory:
                selected = train(p,directory,seed=17,epochs=6,hidden=32,u_hidden=16,
                    successors=successors,checkpoint_start=0,checkpoint_every=6,
                    validation_rounds=[1,1,1])
                arrays,metadata = load_policy(selected,p)
                cost,_ = rollout(p,0,'proposed',picnn=arrays,alpha=metadata['alpha'])
                self.assertTrue(np.isfinite(cost))
                history = json.loads((Path(directory)/'training_history.json').read_text())
                self.assertTrue(np.isfinite(history[-1]['loss'][str(p.T)]))
                self.assertEqual(metadata['settings']['successors'],successors)
                self.assertEqual(metadata['settings']['loss'],'mse')

    def test_replay_fit_uses_mean_squared_error(self):
        net = torch.nn.Sequential(torch.nn.Linear(1,1,bias=False),torch.nn.Flatten(start_dim=0))
        with torch.no_grad():
            net[0].weight.zero_()
        samples = [(np.asarray([0.],dtype=np.float32),float(y)) for y in range(1,6)]
        settings = {**DEFAULTS,'lr':0.,'weight_decay':0.,'grad_steps':1}
        self.assertAlmostEqual(fit(net,samples,settings),11.,places=6)

    def test_training_rejects_other_losses_before_creating_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/'rejected_training'
            with self.assertRaisesRegex(ValueError,'MSE loss only'):
                train(Problem(make_config()),output,loss='huber')
            self.assertFalse(output.exists())


if __name__=='__main__':
    unittest.main(verbosity=2)
