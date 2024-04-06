"""
Created by: Shahd Ahmed
3/23/2024
The program implements Swendsen Wang Algorithm on a 2D lattice
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import random
import lattice
from IPython.display import Video


class SW_algorithm:

    #takes lattice df with random spins 
    def __init__(self, lat, size, T):
        self.lat = lat
        self.size = size
        self.T = T
    def generate_bonds(self):
        """
        The method creates bonds between spins by
        iterating through spins and checking neighbors,
        if the spins are equal, bond is created with a probablity (1 - e^-2J/(k_bT))
        
        @Return: bonds: set of random bond
        """
        
        j = 1 #coupling coeffecient 
        p = 1 - np.exp(-2*j / self.T) #probability, assuming J = 1
        bonds = set() #create a unique set of bonds
        for i in range (self.size):
            for j in range (self.size):
                if i < self.size - 1 and self.lat.iat[i, j] == self.lat.iat[i + 1, j] and random.random() < p:
                    bonds.add(((i, j), (i + 1, j)))
                if j < self.size - 1 and self.lat.iat[i, j] == self.lat.iat[i, j + 1] and random.random() < p:
                    bonds.add(((i, j), (i, j + 1)))
                            
        return bonds
    
    def identify_cluster(self):
    
            """
            The method groups connected sites in a cluster
            @Return: clusters array and labels of each cluster
            """
            bonds = self.generate_bonds()
            clusters = []
            for bond in bonds:
                found = False
                for cluster in clusters:
                    if bond[0] in cluster or bond[1] in cluster: 
                        #check if the bond is connected to this cluster
                        cluster.update(bond)
                        found = True
                        break
                if not found:
                    clusters.append(set(bond)) #make new cluster
            
    #         #assign labels for each site
            labels = np.zeros_like(self.lat)
            for i, cluster in enumerate(clusters):
                for point in cluster:
                    labels[point] = i
    
            return clusters, labels
        
            
    def visualizer(self, df_array, path):
        fps = 15
        nSeconds = 10
        snapshots = df_array

        # First set up the figure, the axis, and the plot element we want to animate
        fig = plt.figure(figsize=(8,8))

        a = snapshots[0]
        im = plt.imshow(a, interpolation='none', aspect='auto',)
        #helper function
        def animate_func(i):
            if i % fps == 0:
                print( '.', end ='' )

            im.set_array(snapshots[i])
            plt.title('Temperature : '+ str(self.T))
            return [im]

        anim = animation.FuncAnimation(
                                       fig, 
                                       animate_func, 
                                       frames = nSeconds * fps,
                                       interval = 1000 / fps, # in ms
                                       )

        
        anim.save(path, fps=fps, extra_args=['-vcodec', 'libx264'])
        plt.close()

    
    def update_clusters(self, steps, path, show_animation=False):
        """
        The method changes the cluster status and flips the atoms consecutively 
        """
        #iterate through clusters, randomly update the sites 
        #pick random cluster
        #change its spins
        #calculate magnetism
        df_array = []
        for i in range(steps):
            clusters, labels = self.identify_cluster()
            num_clusters = len(clusters)
            cluster_id = random.randint(0, num_clusters)

            # Create a copy of the DataFrame before appending
            lat_copy = self.lat.copy()

            for i in range(self.size):
                for j in range(self.size):
                    if labels[i, j] == cluster_id:
                        lat_copy.iat[i, j] = -1 * lat_copy.iat[i, j]
                        
            self.lat = lat_copy
            df_array.append(lat_copy)
            
        magnetism = self.lat.values.sum()
        if show_animation:
            self.visualizer(df_array, path)
        
        return abs(magnetism)
    
    def plot_mag_temp(self, steps, temp_range, path, temp_step=1):
        
        """
        The function runs the algorithm for a range of temperatures and gets
        magnetism corresponding to certain temperature
        @return an array of magnetism values and temperture 
        """
    
        mag = []
        T = np.arange(1, temp_range, temp_step)
    
        for i in T:
            self.T = i
            if self.T ==5:
                mag.append(self.update_clusters(steps, path, show_animation=True))
            else:
                mag.append(self.update_clusters(steps, path))

        plt.plot(T, mag, label='Magnetism')
        plt.xlabel('Temperature')
        plt.ylabel('Magnetism')
        plt.grid()
        plt.legend()
        plt.show()



