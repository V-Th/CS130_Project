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
        # stackMember is an array for faster check whether a node is in stack
        self.stackMember = {}
        # currentSet is used to keep track of current strongly connected set    
        self.currentSet = set()
        # setList is used to keep track of the list of stongly connected sets
        self.setList = []
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
        sccs = set()
        for scc in self.setList:
            if len(scc) == 1:
                continue
            sccs.update(scc)
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
                if child in sccs or child == node:
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
        if node in self.stackMember.keys():
            self.stackMember.pop(node)
    
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
        u = parent_child[1]
        if self.low[u] == self.disc[u]:
            w = None
            while w != u:
                w = self.stack.pop()
                self.currentSet.add(w)
                self.stackMember[w] = False
            self.setList.append(self.currentSet.copy())
            self.currentSet.clear()
        if parent_child[0] is not None:
            self.low[parent_child[0]] = min(self.low[parent_child[0]], self.low[parent_child[1]])
        return []

    def lazy_iter(self, parent_child):
        u = parent_child[1]
        self.disc[u] = self.time
        self.low[u] = self.time
        self.time += 1
        self.stackMember[u] = True
        self.stack.append(u)
 
        to_do_list = []
        post_recur = lambda cell: self.post_recursion(cell)
        to_do_list.append((post_recur, parent_child))
        # Go through all vertices adjacent to this
        for v in self.graph[u]:
            # If v is not visited yet, then recur for it
            if self.disc[v] == -1:
                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                
                recur = lambda child_grandchild : self.lazy_iter(child_grandchild)
                to_do_list.append((recur, (u, v)))
            elif self.stackMember[v]:
                # Update low value of 'u' only if 'v' is still in stack
                # This is a loop as 'u' to 'v' is a back edge
                self.low[u] = min(self.low[u], self.disc[v])
 
        return to_do_list

    def lazy_SCC(self):
        self.time = 0
        self.setList.clear()
        self.stack.clear()
        for n in self.nodes:
            self.disc[n] = -1
            self.low[n] = -1
            self.stackMember[n] = False
        
        to_do = []
        for n in self.nodes:
            if self.disc[n] == -1:
                to_do.extend(self.lazy_iter((None, n)))
            while to_do:
                recur, args = to_do.pop()
                to_do.extend(recur(args))
        self.setList.reverse()
        
    # recursive function that find finds and prints strongly connected components using DFS traversal
    # u --> The vertex to be visited next
    # st --> To store all the connected ancestors (could be part of SCC)

    def SCCUtil(self, u):
        # Initialize discovery time and low value
        self.disc[u] = self.time
        self.low[u] = self.time
        self.time += 1
        self.stackMember[u] = True
        self.stack.append(u)
 
        # Go through all vertices adjacent to this
        for v in self.graph[u]:
            # If v is not visited yet, then recur for it
            if self.disc[v] == -1:
                self.SCCUtil(v)
                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                self.low[u] = min(self.low[u], self.low[v])
            elif self.stackMember[v]:
                # Update low value of 'u' only if 'v' is still in stack
                # This is a loop as 'u' to 'v' is a back edge
                self.low[u] = min(self.low[u], self.disc[v])
 
        # from the head node, pop all descendents that are in loop
        # descendents will have low != disc as the low value is the head
        if self.low[u] == self.disc[u]:
            w = None
            while w != u:
                w = self.stack.pop()
                self.currentSet.add(w)
                self.stackMember[w] = False
            self.setList.append(self.currentSet.copy())
            self.currentSet.clear()
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
            self.stackMember[n] = False
        
        # Call the recursive helper function
        # to find articulation points
        # in DFS tree rooted with vertex 'i'
        for n in self.nodes:
            if self.disc[n] == -1:
                self.SCCUtil(n)
        self.setList.reverse()
