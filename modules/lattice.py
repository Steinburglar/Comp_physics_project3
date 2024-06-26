"""
Lucas Steinberger
3-12-2024
contains class definition, functions, and dependancies for a dataframe representation of a lattice. 
"""

import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numba
from numba import njit
from scipy.ndimage import convolve, generate_binary_structure

class Lattice:

    size = 0
    shape = False
    temp = 0
    
    def __init__(self, J, size = 10, shape = False, rand = True, holes = 0, dim = 2):
        self.J = J
        #initialize lattice grid --> 10x10 square grid filled w zeros
        data = [[0 for _ in range(size)] for _ in range(size)]
        self.size = size
        self.M = size
        self.N = size
        self.shape = shape
        self.lat = pd.DataFrame(data)
            
        for i in range(size):
            j_range = size
            if (shape == True):
                j_range = size - i
            if (dim == 1):
                j_range = 1
            for j in range(j_range):
                if (rand == False):
                    self.lat.at[i, j] = 1
                if (rand == True):
                    num = random.random()
                    if (num < 0.5):
                        self.lat.at[i, j] = -1
                    else:
                        self.lat.at[i, j] = 1
                if (holes > random.random()):
                    self.lat.at[i, j] = 0
                        
    #change spin (takes in a list of coordinates)
    def flip(self, lat_list):
        
        if self.lat.at[lat_list[0], lat_list[1]] != 0:
            self.lat.at[lat_list[0], lat_list[1]] = -1*(self.lat.at[lat_list[0], lat_list[1]])
        """
        else:
            for i in range(len(lat_list)):
                if self.lat.at[lat_list[i][0], lat_list[i][1]] != 0:
                    self.lat.at[lat_list[i][0], lat_list[i][1]] = -1*(self.lat.at[lat_list[i][0], lat_list[i][1]])
        """
    def getE(self, node):
        # we apply the nearest neighbor sum to a 2d lattice
        lattice = self.lat.values
        kern = generate_binary_structure(2, 1)
        kern[1][1] = False
        arr = -lattice * convolve(lattice, kern, mode='constant', cval=0)
        return arr.sum()

    
    def getM(self):
        sum = 0
        size = self.size
        for i in range(size):
            for j in range(size):
                sum += self.lat.at[i, j]
        if sum <0:
            sum = -1*sum
        return sum
        

    def randomize_all(self):
        size = self.size
        for i in range(size):
            for j in range(size):
                if self.lat.at[i,j] !=0:
                    self.lat.at[i, j] = random.choice([1,-1])

    
    def get_lattice(self):
        return self.lat
    
    def set_temp(self, T):
        self.temp = T
    def get_delta(self, node):
        #flips a node or sections of nodes and gets the energy delta
        before= self.getE(node)
        self.flip(node)
        after = self.getE(node)
        return after-before
    
    def num_lattice(self):
        print(self.lat.to_string(header=False, index=False))
    
    def color_lattice(self):
        plt.clf()
        plt.imshow(self.lat)
  
