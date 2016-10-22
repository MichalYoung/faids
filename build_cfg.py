"""
What should the code to build a CFG look like?
"""

from cfg import Node, Edge, CFG, BitVec_Flow_Values
from avail import solve_avail

"""
CFG for this simple program:
(0)   START (pseudo-node where nothing is available) gen={ } kill=Universe
(1)   x = 0                # Generates x1, kills all other x
(2)   while x < 10:        # gen=kill={}
(3)       x = x + 1        # generates x3, kills x1
(4)   return x             # gen=kill={}
"""


cfg = CFG()
s0 = cfg.node("s0: x = 0")
s1 = cfg.node("s1: while x < 10", label="s1")
s2 = cfg.node("s2:    x = x + 1")
s3 = cfg.node("s3: return x", label="s3")
cfg.edge(s0,s1).edge(s1,s2).edge(s2,s3)
cfg.edge(s1,s3)
cfg.edge(s2,s1)

# The potential elements in this problem.
# We'll do an "avail" type analysis, but for
# stores rather than expressions (thus the two
# possible elements are the store in line 1 and the
# store in line 3). 
#
store_values = [ "x0", "x2" ]  # x defined in statement 1 and in statement 3
store_universe = frozenset(store_values)
avail_stores = BitVec_Flow_Values( store_universe )

avail_stores.def_gen(s0, "x0")
avail_stores.def_kill(s0, "x2")
avail_stores.def_gen(s2, "x2")
avail_stores.def_kill(s2, "x0")

# The flow equations for reaching definitions is the same
# as the classic 'avail' analysis.  The only difference is
# that we are tracking 
solve_avail(cfg, avail_stores)
print(avail_stores.label(cfg))


            





