"""
What should the code to build a CFG look like?
"""

from cfg import Node, Edge, CFG, BitVec_Flow_Values
import avail

"""
CFG for this simple program, figure 6.10 of book: 
(START)  static void querionable() {
(A)         int k;
(B)         for (int i=0;          GEN={ i }
(C)                      i<10;
(D)              if (someCondition(i))
(E)                 { k = 0; }     GEN={ k }
(F)              else { k += i }   GEN={ k }
(G)         ++i) }                 GEN={ i }
(H)         System.out.println(k);
"""
cfg = CFG()
nStart = cfg.node("Start")
# nA = cfg.node("(A)  int k; ")
# nB = cfg.node("(B)  for (int i=0;")
# nC = cfg.node("(C) i<10;")
# nD = cfg.node("if (someCondition(i))")
# nE = cfg.node("{ k = 0; }")
# nF = cfg.node("else { k += i }")
# nG = cfg.node(" ++i) }")
# nH = cfg.node(" System.out.println(k);")
nStart = cfg.node("nStart")
nA = cfg.node("nA") 
nB = cfg.node("nB")
nC = cfg.node("nC")
nD = cfg.node("nD")
nE = cfg.node("nE")
nF = cfg.node("nF")
nG = cfg.node("nG")
nH = cfg.node("nH")


cfg.edge(nStart, nA)
cfg.edge(nA,nB).edge(nB,nC).edge(nC,nD)
cfg.edge(nD,nE).edge(nE,nG)
cfg.edge(nD,nF).edge(nF,nG)
# Loop edge
cfg.edge(nC,nH)  # Exit from while loop
cfg.edge(nG,nC)  # Continue while loop

store_values = [ "i", "k" ]  # x defined in statement 1 and in statement 3
store_universe = frozenset(store_values)
avail_stores = BitVec_Flow_Values( store_universe )

avail_stores.def_gen(nB, "i")
avail_stores.def_gen(nE, "k")
avail_stores.def_gen(nF, "k")
avail_stores.def_gen(nG, "i")

def init():
    """HACK"""
    global avail_stores
    avail_stores = BitVec_Flow_Values( store_universe )
    avail_stores.def_gen(nB, "i")
    avail_stores.def_gen(nE, "k")
    avail_stores.def_gen(nF, "k")
    avail_stores.def_gen(nG, "i")
    return True, avail_stores.out.name_map()

def advance():
    """
    One step of solution
    """
    changed = avail.solve_avail_one_step(cfg, avail_stores)
    return changed, avail_stores.out.name_map()



            





