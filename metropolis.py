"""
Metropolis Algorithm class
Shahd Ahmed
3/12/2024


"""



import numpy as np
from scipy import constants
import matplotlib.pyplot as plt
import numba
from numba import njit
import lattic_class.py



class Metropolis:
  
    def __init__(self, lattice):
        self.lattice = lattice
       
    
    def random_node(self):
#       picks a random node in the lattice
        x = random.randint(0, self.lattice.size)
        y = random.randint(0, self.lattice.size)
        node_coor = [x, y]
#       get list of coordinates 
        return node_coor
    
  
    def evaluate_delta(self, node):
        delta = self.lattice.get_delta(node)
        k = constants.k
        if delta <0 or random(0,1) <= np.exp(-delta/(k*self.T)):
            return True
        else:
            return False
    
    #@numba.njit("UniTuple(f8[:], 2)(f8[:,:], i8, f8, f8)", nopython=True, nogil=True)
    def run_metropolis(self, steps):
        temp = []  # List to store temperatures
        energy_array = []  # List to store energy values
        mag_array = []  # List to store magnetization values
        for i in range(0, steps):
            node = self.random_node()
            check = self.evaluate_delta(node)
            if check == True:
                new_lattice = self.lattice.flip(node) #returns new lattice configuration 
                temp.append(T)  # range of temperatures
                energy_array.append(self.lattice.getE(node)) #create an array appends all energies 
                mag_array.append(self.lattice.get_lattice.values.sum())  #append sum of spins
                if()
                self.lattice.color_lattice(new_lattice)
        return temp, energy_array, mag_array
            

    def plot_ene_mag(self, steps):

        temp, energy_array, mag_array = run_metropolis(self, steps)
        fig, ax = plt.subplots(1, 2, figsize=(12,4))
        ax[0].plot(temp, energy_array)
        ax[0].set_xlabel('Temperature')
        ax[0].set_ylabel('Magnetism')
        ax[1].plot(temp, mag_array)
        ax[1].set_xlabel('Temperature')
        ax[1].set_ylabel('Total Energy')
        ax[1].grid()
        ax[0].grid()
        plt.show()
