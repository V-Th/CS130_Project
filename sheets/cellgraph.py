#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict

class _CellGraph():
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
        self.setList = []
        self.sccs = set()
        # st is used to store all the connected ancestors (could be part of SCC)
        self.stack = []
        
    # add edge between node1 and node2
    # node1 depends on the value of node2
    # graph[node2] contains all nodes that depend on it
    def add_edge(self, node1, node2):
        self.graph[node2].add(node1)
        self.nodes.add(node1)
        self.nodes.add(node2)

    def direct_refs(self, nodes: list):
        direct_refs = []
        for node in nodes:
            direct_refs.extend(self.graph[node])
        return direct_refs

    # Iterative dfs search for nodes
    # Takes a list of nodes and finds the nodes that rely on them
    def dfs_nodes(self, remianing: list, visited: list):
        # sccs = set()
        # for scc in self.setList:
        #     if len(scc) == 1:
        #         continue
        #     sccs.update(scc)
        while len(remianing) != 0:
            node = remianing.pop()
            # node_scc = set()
            # for scc in self.setList:
            #     if node in scc:
            #         node_scc = scc
            # If node was visited, it has an earlier dependency
            # It would have been updated twice
            if node in visited:
                visited.remove(node)
            visited.append(node)
            for child in self.graph[node]:
                if child in self.sccs or child == node:
                    continue
                if child not in remianing:
                    remianing.append(child)
    
    # remove a given node from the graph
    def remove_node(self, node):
        for n in self.graph:
            if node in self.graph[n]:
                self.graph[n].remove(node)
        if node in self.nodes:
            self.nodes.remove(node)
        if node in self.disc.keys():
            self.disc.pop(node)
        if node in self.low.keys():
            self.low.pop(node)
        if node in self.in_stack.keys():
            self.in_stack.pop(node)
    
    def __str__(self):
        str = ""
        for e in self.graph:
            str += e.__str__() + ":" 
            for v in self.graph[e]:
                str += " " + v.__str__()
            str += "\n"
            
        return str

    # function to print nodeSet
    def print(self):
        for u in self.nodes:
            print('Node: ', u)
            if (u not in self.graph):
                print('     No edges')
            else:
                for v in self.graph[u]:
                    print('     Edge: ', u, ' ===> ', v)
        print()
        print()
 
    # function to print the set of sccs
    def printSets(self):
        for set in self.setList:
            print('Printing new set')
            print(set)
            print()
        print()

    def post_recursion(self, parent_child):
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
        return []

    def lazy_iter(self, parent_child):
        u = parent_child[1]
        self.disc[u] = self.time
        self.low[u] = self.time
        self.time += 1
        self.in_stack[u] = True
        self.stack.append(u)

        # Create a to_do list of nodes to recur on in main function
        to_do_list = []
        # Add the function to run after all children have been visited to the
        # to_do list to which the children recursion are stacked on top of
        to_do_list.append((self.post_recursion, parent_child))
        # Go through all vertices adjacent to this
        for v in self.graph[u]:
            # If v is not visited yet, then recur for it
            if self.disc[v] == -1:
                # Add recursion on child to the to_do
                to_do_list.append((self.lazy_iter, (u, v)))
            elif self.in_stack[v]:
                # Update low value of 'u' only if 'v' is still in stack
                # This is a loop as 'u' to 'v' is a back edge
                self.low[u] = min(self.low[u], self.disc[v])
 
        return to_do_list

    def lazy_SCC(self):
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
                to_do.extend(self.lazy_iter((None, n)))
            while to_do:
                recur, args = to_do.pop()
                to_do.extend(recur(args))
        
    # recursive function that find finds and prints strongly connected components using DFS traversal
    # u --> The vertex to be visited next
    # st --> To store all the connected ancestors (could be part of SCC)

    def SCCUtil(self, u):
        # Initialize discovery time and low value
        self.disc[u] = self.time
        self.low[u] = self.time
        self.time += 1
        self.in_stack[u] = True
        self.stack.append(u)
 
        # Go through all vertices adjacent to this
        for v in self.graph[u]:
            # If v is not visited yet, then recur for it
            if self.disc[v] == -1:
                self.SCCUtil(v)
                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                self.low[u] = min(self.low[u], self.low[v])
            elif self.in_stack[v]:
                # Update low value of 'u' only if 'v' is still in stack
                # This is a loop as 'u' to 'v' is a back edge
                self.low[u] = min(self.low[u], self.disc[v])
 
        # from the head node, pop all descendents that are in loop
        # descendents will have low != disc as the low value is the head
        if self.low[u] == self.disc[u]:
            w = None
            scc = set()
            while w != u:
                w = self.stack.pop()
                scc.add(w)
                self.in_stack[w] = False
            self.setList.append(scc.copy())
            scc.clear()
            #return scc
 
    # The function to do DFS traversal.
    # It uses recursive SCCUtil()
    def SCC(self):
 
        # Mark all the vertices as not visited
        # and Initialize parent and visited,
        # and ap(articulation point) arrays
        
        self.time = 0
        self.setList.clear()
        self.stack.clear()
        for n in self.nodes:
            self.disc[n] = -1
            self.low[n] = -1
            self.in_stack[n] = False
        
        # Call the recursive helper function
        # to find articulation points
        # in DFS tree rooted with vertex 'i'
        for n in self.nodes:
            if self.disc[n] == -1:
                self.SCCUtil(n)
        self.setList.reverse()
