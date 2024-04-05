"""
Metroplois Algorithm class
Shahd Ahmed
3/12/2024


"""
import numpy as np
import copy
import matplotlib.pyplot as plt
import numba
import random
import matplotlib.animation as animation
import pandas as pd
from IPython.display import Video
from matplotlib.colors import ListedColormap

class Metroplois:
  
    def __init__(self, graph, T):
        self.graph = graph
        self.T = T
    
    def random_node(self):
#       picks a random node in the lattice
        x = random.randrange(0, self.graph.M)
        y = random.randrange(0, self.graph.N)
        node_coor = [x, y]
#       get list of coordinates 
        return node_coor
  
    def evaluate_delta(self, node):
        delta = self.graph.get_delta(node)
        k = 1
        if delta <0 or random.random() <= np.exp(-delta/(k*self.T)):
            return True
        else:
            return False
    
    #@numba.njit("UniTuple(f8[:], 2)(f8[:,:], i8, f8, f8)", nopython=True, nogil=True)
    def run_metroplois(self, steps, path, display=False):
        graph_snapshots_array = []
        for i in range(0, steps):
            node = self.random_node()
            check = self.evaluate_delta(node)
            if check == False:
                self.graph.flip(node) #updates graph back to old lattice configuration
            graph_snapshots_array.append(self.graph.lat.copy())
        if display:
            self.visualizer(graph_snapshots_array, self.T, path,)
            
    
    def visualizer(self, graph_snapshots_array, T, path):
        fps = 30
        nSeconds = 5
        snapshots = graph_snapshots_array

        # First set up the figure, the axis, and the plot element we want to animate
        fig = plt.figure( figsize=(8,8) )

        a = snapshots[0]
        colors = ['blue', 'white', 'red']  # Colors for -1, 0, and 1 respectively
        cmap = ListedColormap(colors)
        im = plt.imshow(a, cmap = cmap, interpolation='none', aspect='auto', vmin=0, vmax=1,)
        #helper function
        def animate_func(i):
            if i % fps == 0:
                print( '.', end ='' )

            im.set_array(snapshots[i])
            plt.title('Temperature : '+ str(T))
            return [im]

        anim = animation.FuncAnimation(
                                       fig, 
                                       animate_func, 
                                       frames = nSeconds * fps,
                                       interval = 1000 / fps, # in ms
                                       )

        anim.save(path, fps=fps, extra_args=['-vcodec', 'libx264'])
        plt.close()
            

                    
    def plot_mag_temp(self, steps, temp_range, path, temp_step=1):
        """
        method to run a metropolis algorithm for a variety of temperatures and plot
        the final magnetism as a function of that temperature
        @param: steps: - int - how many iterations for the algorithm to complete before it is done
        @param: temp_range - list- list of the range of temeratures to be sampled,
        should be [lowest, highest, step]
        """
        mag_array = []  # List to store magnetization values
        temp = []  # List to store temperatures
        for T in range(1, temp_range, temp_step):
            self.graph.randomize_all()
            self.T = T
            if T == 5:
                self.run_metroplois(steps, path, display =True)
            else:
                self.run_metroplois(steps, path)
            temp.append(self.T)  # range of temperatures
            mag_array.append(self.graph.getM())  #append sum of spins

        fig, ax = plt.subplots(figsize=(12,4))
        ax.plot(temp, mag_array)
        ax.set_xlabel('Temperature')
        ax.set_ylabel('Magnetism')
        ax.grid()
        plt.show()



