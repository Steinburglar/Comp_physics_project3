"""
Lucas Steinberger
3-12-2024
Module containing a class for representing a lattice structure ising model as a graph.
"""


import random
import pandas as pd
import lattice
import matplotlib.pyplot as plt
class graph:
    
    def __init__(self, J):
        """
        Init method for a graph calss.
        creates a graph object to represent an arbitrary lattice of 2 or 3 dimensions (only 2D currently implemented)
        @param: J: float
            this is the J value of the lattice model we want to simulate. in physics, this is a property of the material
        """
        self.J = J
        self.vertex = []
        self.adj = []

    def set_J(self, J):
        """
        method to set or change the J value for an ising graph model
        side effect: updates self.J
        """
        self.J = J
    
    

    def initialize(self, lattice, dimension = 2):
        """
        method to build/reset the actual structure of the graph
        @param = lattice: DataFrame
            - lattice is a dataframe representing the physical structure of the ising model. It can be is 2
            or 3 dimensions
        @param: dimension: int (2 or 3)
            tells the method whether to interpret the lattice as 2D or 3D
        """
        # for 2D:
        M, N = lattice.shape
        self.M = M
        self.N = N
        self.adj = adjacency_list(lattice, dimension)
        self.vertex = lattice.values.flatten()

    def flip(self, nodes):
        """
        Method to flip one or more nodes/vertices of the graph
        @param: nodes: This is either a single integer or a list of integers, that are the index of the nodes to be flipped
        side effects: flips nodes
        returns: none
        """
        if isinstance(nodes, int):
            self.vertex[nodes] = -1*self.vertex[nodes]
        else:
            for node in nodes:
                self.vertex[nodes] = -1*self.vertex[nodes]

    def getE(self, nodes):
        """
        Method to find the energy associated with a node or a group of nodes (in the case of a cluster)
        @param: nodes: This is either a single integer or a list of integers, that are the index of the nodes to be flipped
        side effects: none
        returns: energy associated with node/nodes
        """
        node = flattened_index(nodes, self.N) #needs work
        sum = 0 #initialize energy E
        if isinstance(nodes, int): #if just one node
            node = nodes
            for neighbor in self.adj[node]:
                sum += self.vertex[neighbor] * self.vertex[node]

        else: #if multiple nodes
            completed_pairs = [] #keep track of pairs that are already checked
            for node in nodes:
                for neighbor in self.adj(node):
                    pair = [node, neighbor]
                    pair_inv = [neighbor, node]
                    if pair not in completed_pairs or pair_inv not in completed_pairs:
                        sum += self.vertex[node] * self.vertex[neighbor]
                        completed_pairs.append(pair)
        E = self.J*(-1)*(sum)
        return E
    
    def randomize_all(self):
        """
        method to randomly resent all the non-zero entries in the graph vertices."""
        for node in self.vertex:
            if self.vertex[node] != 0:
                node = random.choice([-1, 1])
    
    
    def getM(self):
        """
        method to get the current total magnetism of the lattice/graph
        """
        sum = 0
        for vertex in self.vertex:
            sum += self.vertex
        return sum


    def get_delta(self, node):
            #flips a node or sections of nodes and gets the energy delta
            before= self.getE(node)
            self.flip(node)
            after = self.getE(node)
            return after-before
    
    def flattened_index(self, coords,):
                """
                function to return the flattened index of a point at i, j
                @param: coords: should be list of two elements: i, j, which are the index of the location in a 2d dataframe
                """
                i = coords[0]
                j = coords[1]
                return i*self.N + j

    def unflattened_index(self, node_index):
        """
        returns the coordinates of a node
        """
        i = int(node_index/self.N)
        j = node_index % self.N
        return i, j
    
    def display(self):
        df = self.vertex.reshape(self.M, self.N)
        plt.imshow(df)



     
    
def adjacency_list(lattice, dimension):
            """
            function to build an adjacency out of the lattice. used as part of the graph initialize method.
            returns an M*N dataframe, where the values are lists of the flattened index of the adjacent nodes
            """
            M, N = lattice.shape
            empty_frame = [[[] for _ in range(M)] for _ in range(N)]
            matrix  = pd.DataFrame(empty_frame)
            for i in range(M):
                for j in range(N):
                    neighbors = []
                    if i > 0:
                        neighbors.append(flattened_index([i-1,j], N))
                    if i < (M-2):
                        neighbors.append(flattened_index([i+1,j], N))
                    if j > 0:
                        neighbors.append(flattened_index([i,j-1], N))
                    if j < (N-2):
                        neighbors.append(flattened_index([i,j+1], N))
                    
                    matrix.at[i, j] = neighbors
            adjacency_list = matrix.values.flatten()
            return adjacency_list