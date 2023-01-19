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
        self.st = []
        
    # add edge between node1 and node2
    # node1 depends on the value of node2
    # graph[node2] contains all nodes that depend on it
    def add_edge(self, node1, node2):
        self.graph[node2].add(node1)
        self.nodes.add(node1)
        self.nodes.add(node2)

    # iterative dfs search for nodes
    # takes a list of nodes and finds the nodes that rely on them
    def dfs_nodes(self, found: list, searched: list):
        if len(found) == 0:
            return
        node = found.pop()
        if node in searched:
            searched.remove(node)
        searched.append(node)
        for child in self.graph[node]:
            if child not in found:
                found.append(child)
        self.dfs_nodes(found, searched)
    
    # remove a given node from the graph
    def remove_node(self, node):
        referencing_cells = []
        if node in self.graph:
            referencing_cells = list(self.graph.pop(node))
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
        cells_to_update = []
        self.dfs_nodes(referencing_cells, cells_to_update)
        return cells_to_update
            
    # returns whether node1 connects to node2
    def connected(self, node1, node2):
        if node2 in self.graph[node1]:
            return True
        else:
            return False
    
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
        
    # recursive function that find finds and prints strongly connected components using DFS traversal
    # u --> The vertex to be visited next
    # st --> To store all the connected ancestors (could be part of SCC)

    def SCCUtil(self, u):
 
        # Initialize discovery time and low value
        self.disc[u] = self.time
        self.low[u] = self.time
        self.time += 1
        self.stackMember[u] = True
        self.st.append(u)
 
        # Go through all vertices adjacent to this
        for v in self.graph[u]:
 
            # If v is not visited yet, then recur for it
            if self.disc[v] == -1:
 
                self.SCCUtil(v)
 
                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                self.low[u] = min(self.low[u], self.low[v])
 
            elif self.stackMember[v] == True:
 
                '''Update low value of 'u' only if 'v' is still in stack
                (i.e. it's a back edge, not cross edge).
                Case 2 (per above discussion on Disc and Low value) '''
                self.low[u] = min(self.low[u], self.disc[v])
 
        # head node found, pop the stack and print an SCC
        w = -1  # To store stack extracted vertices
        if self.low[u] == self.disc[u]:
            while w != u:
                w = self.st.pop()
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
        
        self.st.clear()
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
