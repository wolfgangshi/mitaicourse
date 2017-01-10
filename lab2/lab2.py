# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
##    print "BFS from start: %s ==> goal: %s" % (start, goal)
    agenda = [[start]]
    extended_set = set([])
##    statistics = _count()

    while agenda:
        curr_path = agenda.pop() ## list.pop() deletes and returns the last item in the list.
        node = curr_path[-1]
        if node == goal:
            return curr_path
        else:
            if not extended_set.issuperset( set([node]) ):
                extended_set.add(node)
                for n in graph.get_connected_nodes(node):
##                    print "Enqueued: %s" % statistics.next()

                    ## Insert at the start of the agenda.
                    ## FILO for BFS
                    agenda.insert(0, curr_path + [n])

    ## Failed to find the goal
    return []

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
##    print "DFS from start: %s ==> goal: %s" % (start, goal)
    agenda = [[start]]
    extended_set = set([])
##    statistics = _count()

    while agenda:
        curr_path = agenda.pop() ## list.pop() deletes and returns the last item in the list.
        node = curr_path[-1]
        if node == goal:
            return curr_path
        else:
            if not extended_set.issuperset( set([node]) ):
                extended_set.add(node)
                for n in graph.get_connected_nodes(node):
##                    print "Enqueued: %s" % statistics.next()

                    ## Insert at the end of the agenda.
                    ## FIFO for DFS.
                    agenda.insert(len(agenda), curr_path + [n])
    ## Failed to find the goal
    return []



## Now we're going to add some heuristics into the search.
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
##    print "Hill climbing from start: %s ==> goal: %s" % (start, goal)
    agenda = [[start]]
##    statistics = _count()

    while agenda:
        curr_path = agenda.pop() ## list.pop() deletes and returns the last item in the list.
        node = curr_path[-1]
        if node == goal:
            return curr_path
        else:
            neighbours = graph.get_connected_nodes(node)
            neighbours.sort(key = lambda node: graph.get_heuristic(node, goal), reverse = True)
            for n in neighbours:
                if not set(curr_path).issuperset( set([n]) ): ## Reject loops
##                    print "Enqueued: %s" % statistics.next()

                    agenda.insert(len(agenda), curr_path + [n])

    ## Failed to find the goal
    return []

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    """ persist: agenda. The agenda in beam search always contain the k-th best paths for a certain length.
    The algorithm proceeds and extends nodes from the same level (nodes in the agenda) at one time, and update
    the agenda. During this extension and update:
    If the goal is reached, return the path leading to the goal;
    If no goal is found, then extend the path and choose the k-th best if the neighbouring node is neither on the current path nor a dead end.
    """
    print 'beam_width = %s' % beam_width
    agenda = [[start]]
    result_path = []

    while (not result_path):
        if not agenda:
            ## fail to find any solution
            break
        print "agenda at level %s = %s." % (len(agenda[0]), agenda)
        agenda, result_path = _extendForOneLevel(agenda, graph, goal, beam_width)

    return result_path

def _extendForOneLevel(agenda, graph, goal, beam_width):
    """
    Return a tuple of:
    1. the agenda (k-th best paths) for the next level, if the goal is not found in this level; otherwise [].
    2. a result_path when a goal is found, otherwise [].
    """
    accumulatedPaths = []
    while agenda:
        curr_path = agenda.pop() ## list.pop() deletes and returns the last item in the list.
        node = curr_path[-1]
        if node == goal:
            ## We've found a goal.
            return [], curr_path
        else:
            neighbours = graph.get_connected_nodes(node)
            for n in neighbours:
                ## Reject loops and is not and dead end. But we must be careful because a dead end node maybe the goal.
                if (not set(curr_path).issuperset( set([n]) ) ) and ( graph.get_connected_nodes(n) or n == goal) :
                    accumulatedPaths.append( curr_path + [n] )
    accumulatedPaths.sort(key = lambda p: graph.get_heuristic(p[-1], goal), reverse = True )

    return accumulatedPaths[-beam_width:], []

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    length = 0
    while len(node_names) > 1:
        length += graph.get_edge(node_names[0], node_names[1]).length
        node_names = node_names[1:]

    return length


def branch_and_bound(graph, start, goal):
    """
    NOT use extended_set, but reject loop.
    """
    agenda = [[start]]
##    statistics = _count()
    while agenda:
        curr_path = agenda.pop() ## list.pop() deletes and returns the last item in the list.
        node = curr_path[-1]
        if node == goal:
            return curr_path
        else:
             for n in graph.get_connected_nodes(node):
##                    print "Enqueued: %s" % statistics.next()
                 if not set(curr_path).issuperset( set([n]) ):
                     agenda.append(curr_path + [n])
                     agenda.sort(key = lambda path: path_length(graph, path), reverse = True)

    ## Failed to find the goal
    return []

def a_star(graph, start, goal):
    """
    An A* always use an extended_set
    """
    agenda = [[start]]
    extended_set = set([])

    while agenda:
        curr_path = agenda.pop()
        node = curr_path[-1]
        if node == goal:
            return curr_path
        else:
            if not extended_set.issuperset(set([node])):
                extended_set.add(node)
                agenda.extend( [curr_path + [n] for n in graph.get_connected_nodes(node)] )
                agenda.sort(key = lambda path: path_length(graph, path) + graph.get_heuristic(path[-1], goal), reverse = True)

    ## Failed to find the goal
    return []

## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    for node in graph.nodes:
        shortest_path = branch_and_bound(graph, node, goal)
        if graph.get_heuristic(node, goal) > path_length(graph, shortest_path):
            return False
    return True

def is_consistent(graph, goal):
    raise NotImplementedError

HOW_MANY_HOURS_THIS_PSET_TOOK = ''
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''

def _count():
    i = 0
    while True:
        i += 1
        yield i


if __name__ == '__main__':
    assert((not _isContainInSet(3, set([1,2]))) )
    assert(_isContainInSet(3, set([3])))

    assert(_nodeToExtend(['1','2','3']) == '3')
    assert(_nodeToExtend(['3']) == '3')
