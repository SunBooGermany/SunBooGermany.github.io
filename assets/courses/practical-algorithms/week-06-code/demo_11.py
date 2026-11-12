"""Session demonstration; run after predicting each printed result."""
from solutions import *

edges=[[2,0],[2,1],[3,2]]; print(course_order(4,edges)); print(acyclic_dfs_small(4,edges)); print(can_finish(2,[[0,1],[1,0]]))
