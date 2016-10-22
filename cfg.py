"""
Control flow graph data structure(s).
"""

class Node:
    """
    A node (statement, block, etc) in the control flow graph.
    Public attributes are name, successors, predecessors
    """
    
    def __init__(self, name):
        self.name = name
        self.cfg = None   # Changed when inserted into CFG
        self.predecessors = [ ]
        self.successors = [ ] 

    def in_cfg(self, cfg):
        self.cfg = cfg

    def add_successor(self, other):
        self.successors.append(other)

    def add_predecessor(self, other):
        self.predecessors.append(other)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Edge:
    """A directed edge (step in control flow) from the CFG"""
    def __init__(self, from_node, to_node, cfg_context):
        self.from_node = from_node
        self.to_node = to_node
        self.cfg = cfg_context

class CFG:
    """
    The control flow graph of a program. Program nodes
    and edges.  Since we may compute multiple properties
    over the same CFG, properties associated with a CFG
    are kept elsewhere.

    Successor and predecessor relations can be kept here. 
    """
    def __init__(self):
        self.nodes = [  ] # List of node objects
        self.edges = [  ] # List of edge objects
        self.labeled_nodes = { }  # Map from labels to node objects

    def node(self, name, label=None):
        new_node = Node(name)
        self.nodes.append(new_node)
        if label:
            self.labeled_nodes[label] = new_node
        return new_node

    def find_node(self, node_name):
        """Returns node object from its name, 
           or throws exception if node doesn't exist.
        """
        return self.labeled_nodes[node_name]

    def edge(self, from_node, to_node):
        """Create a CFG edge from node named from_node_name
           to node named to_node_name.
        """
        if type(from_node) == str:
            from_node = self.find_node(from_node)
        if type(to_node) == str:
            to_node = self.find_node(to_node)
        # The source and sink node belong to this graph
        self.edges.append(Edge(from_node, to_node, self))
        from_node.add_successor(to_node)
        to_node.add_predecessor(from_node)
        return self  # For chaining method calls

class BitVec_Prop:
    """
    A boolean property that we can calculate with respect to
    a CFG using a classical gen/kill iterative data flow analysis.

    cfg, universe, initial are public attributes
    out should be accessed through getter and setter
    """
    def __init__(self, initial):
        # The initial value of this property, as a set
        self.initial = initial    
        # Current values (default to self.initial)
        self.val = { }

    def get(self, node):
        """ Current value of bitvec property at node """
        if node in self.val:
            return self.val[node]
        else:
            return self.initial

    def set(self, node, value):
        """ New current value of bitvec property at node """
        self.val[node] = value

    def __repr__(self):
        return repr(self.val)

    def __str__(self):
        return str(self.val)

def to_frozen_set( val ):
    """
    For defining gen and kill, it is convenient to permit not
    only iterables (which can be converted to frozenset with the
    constructor) but also strings representing singletons.
    """
    if isinstance(val, str):
        return frozenset([ val ])
    else:
        return frozenset(val)

class BitVec_Flow_Values:
    """
    The system of values for a particular flow analysis.
    Includes gen (always defaults to empty), kill (always defaults to empty),
    and out (may default to empty or to the universe).
    """
    def __init__(self, initial):
        """
        The initial value here is for the "out" value on a node.
        Gen and Kill sets always default to empty for convenience.
        """
        self.initial = initial
        self.out = BitVec_Prop(initial)
        self.gen = BitVec_Prop( frozenset() )
        self.kill = BitVec_Prop( frozenset() )

    # Write and read the 'gen' sets
    # As a convenience, elements may be a list,
    # a set, or a string indicating a singleton set
    def def_gen(self, node, elements):
        self.gen.set(node, to_frozen_set(elements))

    def gen(self, node):
        return self.gen.get(node)

    # Write and read the 'kill' sets
    def def_kill(self, node, elements):
        self.kill.set(node, to_frozen_set(elements))

    def kill(self, node):
        return self.kill.get(node)

    def __repr__(self):
        return str(self.out)

    def __str__(self):
        return str(self.out)

    def label(self, cfg):
        """
        String representation of CFG nodes (in order) labeled
        with flow values.
        """
        rep = ""
        nl = ""
        for node in cfg.nodes:
            rep += nl + "{}\tgen={}\tkill={}\tout={}".format(
                node, 
                set(self.gen.get(node)),
                set(self.kill.get(node)),
                set(self.out.get(node)))
            nl = "\n"
        return rep
