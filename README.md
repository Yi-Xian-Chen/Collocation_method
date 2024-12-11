# Collocation Method for Solving RTBP orbits

This python code solves closed orbits in a given potential system using a novel spectral or collocation method, with application to the Restricted Three-Body Problem, where tidally distorted orbits typically belong to either the circumstellar (S-type) or circumbinary (P-type family).
Detailed science and method see companion project report.

## Installation

### Prerequisites

To install this python package properly/efficiently, you will need

- Python 3.8 or higher
- pip3
- build
- make

### Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/Yi-Xian-Chen/Collocation_method.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Collcation_method
   ```

3. Run Makefile
   ```bash
   make install
   ```

## Usage

As long as python is included in your system's `PATH`, 
you will be able to execute functions defined in the `orbit/*.py` modules from anywhere. 
For example, you can manipulate orbits using Python or a Jupyter Notebook as shown below:


```python
import orbit
# Create an instance of class CRTBP_orbits with your arguments
O = orbit.CRTBP_orbits(*args)

# Solve the orbit equations
O.solve()

# Visualize the results
O.plot()
```

To execute simply the main function in `orbit/__init__.py`, apply command

```bash
orbitrun 
```

under some run directory `rundir/`, which is equivalent to executing in Python

```python
import orbit
orbit.main()
```

## Input

The `main` function reads input parameters from `rundir/input.txt`. Users can configure parameters for the RTBP in a co-rotating reference frame centered on the center of mass (CoM) of the system. 

- **Primary mass fraction**: `m1`  

- **Parameters for the list of angular frequencies**: `omegamin, omegamax, omegaN`

- **Number of collocation points in phase space**: `N`

Detailed instructions for setting up additional parameters can be found in the example file `test/input.txt`.

## Output

Executing the `main` function will generate the following outputs in the `rundir` directory:

- **`X.txt`** and **`Y.txt`**: These files contain the coordinates of the closed orbits over one period, based on the list of angular frequencies (A.K.A periods) defined in `test/input.txt`. 

- **`output.pdf`**: A visual representation of all the orbits, with respect to locations of primary and secondary.

While the PDF provides an overview, users can perform detailed analysis of the `X.txt` and `Y.txt` files using external Python scripts or other tools.


## Test

To run the tests provided in the repository after installation, use one of the following methods:

1. Using Python directly:  
   ```bash
   cd test
   python orbit_test.py
    ```

2. If `pytest` is installed:  
   ```bash
   pytest
    ```

## Uninstall

```bash
    make clean
    make uninstall
```


## Contributing

Users interested in contributing are welcome to contact me at yc9993@princeton.edu
I'm currently working on the extension to eccentric binary systems.

