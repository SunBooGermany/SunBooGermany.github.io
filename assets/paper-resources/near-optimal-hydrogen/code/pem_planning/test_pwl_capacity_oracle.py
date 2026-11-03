import unittest
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix,vstack
from .model import Config,Scenario
from .pwl_capacity_oracle import PWLCapacityOracle
from .pwl_planning import build


class PWLProjectionTests(unittest.TestCase):
    def setUp(self):
        self.cfg=Config(pem_cold_start_fraction=0.,time_limit_s=30,solver_threads=1)
        rng=np.random.default_rng(943)
        self.scenarios=[Scenario(str(k),rng.uniform(0,.7,16),rng.uniform(0,.8,16)) for k in range(3)]

    def full(self,oracle,integer=False,direction=None,cap=None,unbounded_design=False):
        bounds=None if unbounded_design else np.array([[0,2000],[0,2000],[0,1000],[0,1e7]])
        m,ids,_,offset,_=build(self.cfg,self.scenarios,bounds,integer_wind=integer)
        A=coo_matrix((m.data,(m.rows,m.cols)),shape=(len(m.lo),len(m.lb))).tocsc()
        lo,hi=np.asarray(m.lo),np.asarray(m.hi)
        if cap is not None:
            row=np.zeros(len(m.lb));row[ids]=oracle.cost/1e6
            A=vstack([A,coo_matrix(row[None,:])]).tocsc()
            lo=np.r_[lo,-np.inf];hi=np.r_[hi,(cap-oracle.constant)/1e6]
        c=np.zeros(len(m.lb));c[ids]=oracle.cost/1e6 if direction is None else direction
        r=milp(c,integrality=m.integer,bounds=Bounds(m.lb,m.ub),constraints=LinearConstraint(A,lo,hi),
               options={'mip_rel_gap':1e-10,'time_limit':30})
        self.assertEqual(r.status,0)
        return r,float(oracle.cost@r.x[ids]+oracle.constant)

    def test_full_integer_model_without_artificial_capacity_upper_bounds(self):
        o=PWLCapacityOracle(self.cfg,self.scenarios)
        _,bounded=self.full(o,integer=True)
        _,unbounded=self.full(o,integer=True,unbounded_design=True)
        self.assertAlmostEqual(bounded,unbounded,delta=.05)
        m,ids,_,_,size=build(self.cfg,self.scenarios,bounds=None,integer_wind=True)
        self.assertTrue(np.isinf(m.ub).all())
        self.assertEqual(m.lb[ids[2]],0)
        self.assertEqual(size['integer_variables'],1)
        self.assertEqual(size['operating_binary_variables'],0)

    def test_hourly_pwl_projection_matches_extensive_cost_milp_and_support(self):
        o=PWLCapacityOracle(self.cfg,self.scenarios)
        p=o.solve();_,full=self.full(o)
        self.assertAlmostEqual(p['cost'],full,delta=.03)
        p=o.solve_milp();_,full=self.full(o,integer=True)
        self.assertAlmostEqual(p['cost'],full,delta=.05)
        o.witness(p['x'])
        cap=p['cost']*1.02
        for direction in [np.array([1.,0,0,0]),np.array([0.,0.,-1.,0]),np.array([.2,-.1,1.,1e-4])]:
            projected=o.solve(direction,cap=cap)
            full,_=self.full(o,direction=direction,cap=cap)
            self.assertAlmostEqual(projected['objective'],full.fun,delta=1e-5)
            o.witness(projected['x'])

    def test_cuts_are_global_not_local_tangents_with_wrong_sign(self):
        o=PWLCapacityOracle(self.cfg,self.scenarios)
        o.separate(np.array([80.,10.,1.,50.]))
        rng=np.random.default_rng(942)
        from .continuous_oracle import SCALE
        for _ in range(12):
            x=np.array([500.,500.,100.,1e6])*rng.uniform(.8,1.5,4)
            self.assertLessEqual(o.separate(x,add=False)[0],1e-4)
            self.assertLessEqual(float(np.max(np.asarray(o.A)@(x/SCALE)-o.b)),1e-7)


if __name__=='__main__':unittest.main()
