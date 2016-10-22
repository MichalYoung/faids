"""
Simple iterative data flow analysis of
available expressions (or other properties
that use the same flow equations, such as
reaching definitions)
"""

import logging
logging.basicConfig(level=logging.WARN)

def meet_as_intersect( property, nodes ):
    """
    The flow analysis 'meet' operation as intersection
    of values flowing in from neighboring nodes. 
    Includes special case for source or sink nodes.
    """
    logging.debug("Meet operation on nodes {}".format(nodes))
    # Special case for source or sink nodes, where there
    # is no flow in.  This differs from the mathematical
    # definition of intersection over no elements. 
    if len(nodes) == 0:
        return set()
    # Otherwise we take the intersection of incoming values
    # (which may be coming from predecessors or successors)
    meet = property.out.get(nodes[0])
    for neighbor in nodes[1:]:
        meet = meet & property.out.get(neighbor)
    logging.debug("Computed meet as {}".format(meet))
    return meet

def solve_avail(cfg, avail):
    """
    Maybe this will help me see how to factor it out.
    """
    logging.debug("Beginning solver")
    # Init has been done
    # Gen and kill have been defined
    # We'll initially use a stupid iteration scheme
    changed = True
    while changed:
        changed = False
        for node in cfg.nodes:
            logging.debug("Applying meet/join for node {}".format(node))
            new_value = ((meet_as_intersect(avail, node.predecessors)
                          - avail.kill.get(node)) | avail.gen.get(node))
            if new_value != avail.out.get(node):
                changed = True
                avail.out.set(node,new_value)

