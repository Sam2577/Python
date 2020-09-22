from __future__ import print_function
import unittest
import sys

class graph:
    def __init__(self, nodes=None, edges=None):
        self.__nodes = set()
        self.__edges = set()
        
        if nodes:
            for node in nodes:
                self.__nodes.add(node)
        
        if edges:
            for edge in edges:
                self.__edges.add(edge)

    # return immutable tuples
    def nodes(self):
        return tuple(self.__nodes)
    
    def edges(self):
        return tuple(self.__edges)
    
    def add_node(self, node):
        self.__nodes.add(node)
        
    def add_edge(self, edge):
        self.__edges.add(edge)
        
    def adjacent(self, node):
        result = ()
        for edge in self.__edges:
            if edge[0] in result or edge[1] in result: continue
            if edge[0] == node: result += (edge[1],)
            if edge[1] == node: result += (edge[0],)
        return(result)

    """Find a path through a graph"""
    def DFS(self, start, target):
        stack = [start]
        visited = []

        while stack:
            current = stack.pop()
            visited.append(current)

            if current == target:
                return visited

            for v in self.adjacent(current):
                if v not in visited:
                    stack.append(v)

        return None

    def rDFS(self, start, target, visited):
        visited.append(start)

        if start == target: return visited

        for v in self.adjacent(start):
            if v not in visited:
                return(self.rDFS(v, target, visited))

        return None

    def BFS(self, start, target):
        queue = [start]
        visited = []

        while queue:
            current = queue.pop(0)
            if current in visited: continue
            visited.append(current)

            if current == target: return visited

            for v in self.adjacent(current):
                if v not in visited and v not in queue:
                    queue.append(v)

        return None

    def __str__(self):
        return("nodes:" + str(self.nodes()) + ", edges:" + str(self.edges()))

g = graph([1,2,3], [(1,3),(2,3)])
g.add_node(4)
g.add_edge((4,2))
g.add_node(5)
g.add_node(6)
g.add_node(7)
#g.add_edge((3,5))
g.add_edge((4,6))
g.add_edge((5,7))
g.add_edge((6,7))
g.add_node(8)
g.add_edge((7,8))
print(g.DFS(1,5))

l = graph(['a','b','c'], [('a','b'),('a','c')])
print(l.rDFS("b","c", []))
