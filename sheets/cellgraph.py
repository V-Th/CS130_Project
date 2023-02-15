'''
The module implements a graph that keeps track of all the cell references.
This detects loops and finds reference cells to update should one or several
be updated at once.
'''
from collections import defaultdict

class _CellGraph():
    '''
    The class that keeps track of all the cell references, detects loops, and
    reference trees of cells to update.
    '''
    def __init__(self):
        # stores dictionary of sets to store edges
        self.graph = defaultdict(set)
        # stores the nodes of the graph
        self.nodes = set()
        # disc is used to store discovery times of visited vertices
        self.disc = {}
        # low is used to store earliest visited node for each node
        # earliest visited vertex is the vertex with minimum discovery
        # time that can be reached from subtree rooted with current vertex
        self.low = {}
        # time is used to keep track of discovery time
        self.time = 0
        # in_stack is an array for faster check whether a node is in stack
        self.in_stack = {}
        # setList and sccs is used to keep track of the list of stongly connected sets
        self.sccs = set()
        # st is used to store all the connected ancestors (could be part of SCC)
        self.stack = []

    # add edge between node1 and node2
    # node1 depends on the value of node2
    # graph[node2] contains all nodes that depend on it
    def add_edge(self, node1, node2):
        '''
        Adds an edge between cells
        '''
        self.graph[node2].add(node1)
        self.nodes.add(node1)
        self.nodes.add(node2)

    def direct_refs(self, nodes: list):
        '''
        Finds the list of cells that reference the given list of cells.
        It only finds immediate references.
        '''
        direct_refs = []
        for node in nodes:
            direct_refs.extend(self.graph[node])
        return direct_refs

    def bfs_nodes(self, remaining: list, visited: list):
        '''
        A breadth-first search algorithm used to find the list of cells
        whose values will change based on the change of one cell.
        '''
        while remaining:
            node = remaining.pop(0)
            # If node was visited, it has an earlier dependency
            # It would have been updated twice
            if node in visited:
                visited.remove(node)
            visited.append(node)
            for child in self.graph[node]:
                if child in self.sccs or child == node:
                    continue
                if child not in remaining:
                    remaining.append(child)

    # remove a given node from the graph
    def remove_node(self, node):
        '''
        Removes an edge between two cells.
        '''
        for a_node in self.graph:
            if node in self.graph[a_node]:
                self.graph[a_node].remove(node)
        if node in self.nodes:
            self.nodes.remove(node)
        if node in self.disc:
            self.disc.pop(node)
        if node in self.low:
            self.low.pop(node)
        if node in self.in_stack:
            self.in_stack.pop(node)

    def post_recursion(self, parent_child, _):
        '''
        The latter half in the recursion process which checks for whether the
        cell is the head to a loop.
        '''
        parent = parent_child[0]
        child = parent_child[1]
        scc = set()
        if self.low[child] == self.disc[child]:
            in_scc = None
            while in_scc != child:
                in_scc = self.stack.pop()
                scc.add(in_scc)
                self.in_stack[in_scc] = False
            if len(scc) > 1:
                self.sccs.update(scc)
            scc.clear()
        if parent is not None:
            self.low[parent] = min(self.low[parent], self.low[parent])

    def lazy_iter(self, parent_child, to_do):
        '''
        The first half to the recursion process which updates the cell explored
        and calls the recursion on its children.
        '''
        child = parent_child[1]
        self.disc[child] = self.time
        self.low[child] = self.time
        self.time += 1
        self.in_stack[child] = True
        self.stack.append(child)

        # Add the function to run after all children have been visited to the
        # to_do list to which the children recursion are stacked on top of
        to_do.append((self.post_recursion, parent_child))
        # Go through all vertices adjacent to this
        for g_child in self.graph[child]:
            # If v is not visited yet, then recur for it
            if self.disc[g_child] == -1:
                # Add recursion on child to the to_do
                to_do.append((self.lazy_iter, (child, g_child)))
            elif self.in_stack[g_child]:
                # Update low value of 'u' only if 'v' is still in stack
                # This is a loop as 'u' to 'v' is a back edge
                self.low[child] = min(self.low[child], self.disc[g_child])

    # pylint: disable=C0103
    def lazy_SCC(self):
        '''
        The SCC algorithm that finds all SCC's which are loops. It avoids the
        recursion limit by having all recursion calls passed back to it so
        that it may call them instead.
        '''
        self.time = 0
        self.sccs.clear()
        self.stack.clear()
        for n in self.nodes:
            self.disc[n] = -1
            self.low[n] = -1
            self.in_stack[n] = False

        # A to_do list to perform recursions without creating frames
        to_do = []
        for n in self.nodes:
            if self.disc[n] == -1:
                self.lazy_iter((None, n), to_do)
            while to_do:
                recur, args = to_do.pop()
                recur(args, to_do)
