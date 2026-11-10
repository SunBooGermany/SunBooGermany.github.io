"""Session demonstration; run after predicting each printed result."""
from solutions import *

s=MinStack()
for value in [2,2,5]: s.push(value)
s.pop(); s.pop(); print(s.getMin()); print(rpn(["9","4","-","-2","/"]))
