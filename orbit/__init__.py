__version__ = "0.0.1"
__author__ = "Yixian Chen"
__email__ = "yc9993@princeton.edu"
__all__ = ["help_info", "collocation_matrix", "CRTBP_orbits","main","read_input_file"]



from .matrix import collocation_matrix
from .orbits2D import CRTBP_orbits

import numpy as np
import matplotlib.pyplot as plt

def help_info():
    """ Print Basic Help Info """

    print("""
    **************************************************************************
    * 
    * A code to calculate CRTBP orbits.
    * Author: Yixian Chen
    * Current Version: 0.0.1
    * Note: This package is still under active development and we welcome
    *       any comments and suggestions.
    **************************************************************************
    """)


def read_input_file(filename):
    """Reads input parameters from a file."""
    params = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):  # Skip empty or commented lines
                continue
            key, value = line.split()
            if key in ['m1', 'omegamin', 'omegamax', 'h', 'tol']:
                params[key] = float(value)
            elif key in ['N', 'maxit', 'omegaN']:
                params[key] = int(value)
            elif key == 'type':
                params[key] = bool(int(value))
    return params

def main(input_file='input.txt', output_file='output.pdf'):
    """Main function to read parameters, iterate, and save results."""
    params = read_input_file(input_file)
    
    # Extract parameters
    m1, h, tol, N, maxit, type = params["m1"], params["h"], params["tol"], params["N"], params["maxit"], params["type"]
    omegamin, omegamax, omegaN = params["omegamin"], params["omegamax"], params["omegaN"]
    
    # Generate omega values
    omega_values = np.linspace(omegamin, omegamax, omegaN)
    
    # Iterate over omega values and solve
    for omega in omega_values:
        orbit = CRTBP_orbits(m1=m1, omega=omega, h=h, tol=tol, N=N, maxit=maxit, type=type)
        orbit.solve()
        orbit.plot()

    
    
    plt.scatter([m1],[0],label="$M_2$",color="red",marker="x",s=100)
    plt.scatter([m1-1],[0],label="$M_1$",color="red",s=100)
    #locations of M1 and M2

    plt.xlabel("$x$",fontsize=12)
    plt.ylabel("$y$",fontsize=12)
    plt.legend(loc="upper right")
    plt.axis("equal")
    plt.legend()
    plt.savefig(output_file)
    # Save output plot

    #new_orbit.save()

