import numpy as np


def collocation_matrix(N:int): 

    D=[]
    for j in range(N):
        Dj=[]
        for k in range(N):
            Dj.append(0) if (j==k) else Dj.append(0.5*(-1)**(j-k)/np.tan(np.pi*(j-k)/N))
        D.append(Dj) #initialize the first-order matrix
    D=np.mat(D) #change D into matrix form


    D2=[]
    for j in range(N):
        D2j=[]
        for k in range(N):
            D2j.append((-N**2-2)/12) if (j==k) else D2j.append(0.5*(-1)**(j-k+1)/np.sin(np.pi*(j-k)/N)**2)
        D2.append(D2j) #initialize the second-order collocation matrix of rank N
    D2=np.mat(D2) #change D2 into matrix form
    return D, D2