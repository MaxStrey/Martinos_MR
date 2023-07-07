import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

N_spins = 81  # Number of spins in each direction
# Create the phantom
phantom = np.ones((N_spins, N_spins), dtype=np.complex128)  # All spins start in equilibrium state
plt.imshow(np.abs(phantom), cmap='gray')

gamma = 42.58e6  # Gyromagnetic ratio for hydrogen in Hz/T
G = 1e-3  # Gradient strength in T/m

# Load the CSV B0 data into a NumPy array
B0 = np.genfromtxt('2Dslice.csv', delimiter=',')

# Calculate the Larmor frequency
omega0 = B0 * gamma

# Calculate the magnetic field strength