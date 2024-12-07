import numpy as np
from matplotlib import pyplot as plt
#from matrix import collocation_matrix
from .matrix import collocation_matrix


class CRTBP_orbits:  # 2D - Newton Raphson method  
    
    def __init__(self, m1: float=1.0, omega: float= 3.0, h: float = 1.0, tol: float = 1e-12, N: int = 100, maxit: int = 100, type: bool = 0):
        # m1: mass fraction of the binary component on the left (between 0 and 1)
        # omega: two_pi over period
        # h: step fraction for N-R iteration (between 0 and 1), or learning rate
        # tol: numerical tolerance
        # N: number of points that needs to be solved
        # maxit: maximum number of iterations
        # type: 0 for CBD and 1 for CSD

        self.m1 = m1
        self.m2 = 1 - m1  # mass fraction of the right component
        self.x1 = -self.m2  # x coordinate of m2
        self.x2 = m1  # x coordinate of m1
        self.h = h
        self.tol = tol
        self.omega = omega
        self.N = N  
        self.X = np.zeros((self.N, 1))  # to store the x solution as a function of phase
        self.Y = np.zeros((self.N, 1))  # to store the y solution as a function of phase
        self.stable = False  # stability
        self.maxit = maxit
        self.D, self.D2 = collocation_matrix(self.N)
        self.type = type 
        
        # Initialize orbits as circular 
        radius = (1 / (self.omega + 1) ** 2) ** (1 / 3) if self.type == 0 else (m1 / (self.omega + 1) ** 2) ** (1 / 3)   # compute radius of Keplerian orbit around CoM or m1
        for p in range(self.N):
            angle = 2 * np.pi * p / self.N
            self.X[p] = radius * np.cos(angle) if self.type == 0 else radius * np.cos(angle) + self.x1
            self.Y[p] = radius * np.sin(angle)

    
    
    def F2D(self):
        # The force functions for CBD problem
        x, y = self.X, self.Y
        fx = np.zeros((self.N, 1))
        fy = np.zeros((self.N, 1))
        
        # Precompute distances and common terms to avoid redundancy
        dist1 = np.sqrt((x - self.x1) ** 2 + y ** 2)
        dist2 = np.sqrt((x - self.x2) ** 2 + y ** 2)
        dist1_cubed = dist1 ** 3
        dist2_cubed = dist2 ** 3
        
        for i in range(self.N):
            fx[i] = (x[i] - self.x1) * self.m1 / dist1_cubed[i] + (x[i] - self.x2) * self.m2 / dist2_cubed[i]
            fy[i] = y[i] * self.m1 / dist1_cubed[i] + y[i] * self.m2 / dist2_cubed[i]
        
        return fx, fy
    
    def solvefounctionx(self):
        # The x equation of motion residues
        f = self.omega**2 * self.D2 * self.X - 2 * self.omega * self.D * self.Y - self.X + self.F2D()[0]
        return f
    
    def solvefounctiony(self):   
        # The y equation of motion residues
        f = self.omega**2 * self.D2 * self.Y + 2 * self.omega * self.D * self.X - self.Y + self.F2D()[1]
        return f

    
    def solve(self):
        # Solve the orbit until self.X and self.Y converge
        num: int = 0  # Keep track of iteration steps
        
        Fx, Fy = self.solvefounctionx(), self.solvefounctiony()
        
        # Calculate the residues as an error function
        errorfunc = np.sqrt(np.sum(np.array(Fx)**2 + np.array(Fy)**2))
        
        while errorfunc > self.tol:
            # If the error function is still larger than the tolerance
            Jacobix = self.D2 * self.omega**2 - np.eye(self.N)
            Jacobiy = self.D2 * self.omega**2 - np.eye(self.N)
            Jacobi = np.zeros((2 * self.N, 2 * self.N))  # Calculate a "large" Jacobian 2N*2N
            
            for i in range(self.N):
                for j in range(self.N):
                    Jacobi[i, j] = Jacobix[i, j]
                    Jacobi[i + self.N, j + self.N] = Jacobiy[i, j]
                    Jacobi[i, j + self.N] = -2 * self.omega * self.D[i, j]
                    Jacobi[i + self.N, j] = 2 * self.omega * self.D[i, j]
            
            for i in range(self.N):
                Jacobi[i, i] += self.m1 / ((self.X[i] - self.x1)**2 + self.Y[i]**2)**(1.5) * \
                    (1 - 3 * (self.X[i] - self.x1)**2 / ((self.X[i] - self.x1)**2 + self.Y[i]**2)) + \
                    self.m2 / ((self.X[i] - self.x2)**2 + self.Y[i]**2)**(1.5) * \
                    (1 - 3 * (self.X[i] - self.x2)**2 / ((self.X[i] - self.x2)**2 + self.Y[i]**2))
                
                Jacobi[i + self.N, i] += -3 * (self.m1 * (self.X[i] - self.x1) * self.Y[i] / \
                    ((self.X[i] - self.x1)**2 + self.Y[i]**2)**(2.5) + self.m2 * (self.X[i] - self.x2) * self.Y[i] / \
                    ((self.X[i] - self.x2)**2 + self.Y[i]**2)**(2.5))
                
                Jacobi[i + self.N, i + self.N] += self.m1 / ((self.X[i] - self.x1)**2 + self.Y[i]**2)**(1.5) * \
                    (1 - 3 * self.Y[i]**2 / ((self.X[i] - self.x1)**2 + self.Y[i]**2)) + \
                    self.m2 / ((self.X[i] - self.x2)**2 + self.Y[i]**2)**(1.5) * \
                    (1 - 3 * self.Y[i]**2 / ((self.X[i] - self.x2)**2 + self.Y[i]**2))
                
                Jacobi[i, i + self.N] += -3 * (self.m1 * (self.X[i] - self.x1) * self.Y[i] / \
                    ((self.X[i] - self.x1)**2 + self.Y[i]**2)**(2.5) + self.m2 * (self.X[i] - self.x2) * self.Y[i] / \
                    ((self.X[i] - self.x2)**2 + self.Y[i]**2)**(2.5))
            
            Ftotal = np.append(np.array(Fx), np.array(Fy))
            # Put solution of X, Y together into a big vector (X, Y)
            Ftotal = np.mat(Ftotal)
            ab = np.array(-np.linalg.inv(Jacobi) * Ftotal.T)
            # (delta X, delta Y) = J^-1 * Residue for (X, Y)
            abx = ab[0:self.N]
            aby = ab[self.N:2 * self.N]
            # Separate delta X and delta Y
            for i in range(self.N):
                self.X[i] = self.X[i] + self.h * abx[i]
                self.Y[i] = self.Y[i] + self.h * aby[i]
            # Iterate with X -> X + h*delta X, Y -> Y + h*delta Y
            Fx, Fy = self.solvefounctionx(), self.solvefounctiony()
            # Calculate residue again
            errorfunc = np.sqrt(np.sum(np.array(Fx)**2 + np.array(Fy)**2)) #L2 loss function
            # Calculate error function again
            num += 1   
            if num == self.maxit:  # Maximum iteration step
                break
        
        print("omega = " + str(self.omega))
        print('iterations:', num)
        #print("final length of residue is = " + str(errorfunc)) #should write them as history variables
        return


    def plot(self):
        plt.plot(np.append(self.X,self.X[0]) , np.append(self.Y, self.Y[0]), ls = "--", label="$\omega =$"+str(self.omega))
        return


