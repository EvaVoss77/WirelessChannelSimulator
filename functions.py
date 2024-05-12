from scipy import optimize as opt
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize as opt
from scipy import special as sp
from turtle import pos
from matplotlib.axis import XAxis


def genScat(Ns,Rc,Cc):
    """ FUNCTION genScat(Ns, Rc, Cc)
    This function returns an array of N x 2. Each row represents the position
    (x,y) of a reflector on the plane. These reflectors are distributed
    randomly and uniformly inside circles with radii given by the
    vector Rc (cluster radii), and within each cluster, there are a certain number
    of reflectors given by the vector of reflector quantities per cluster Ns.
    Cc is an array with a number of rows equal to the number of clusters
    and whose rows are the positions (x,y) of the cluster centers.
    Example:
    --------
    Ns = [20, 20, 20];
    Rc = [20, 20, 20];
    Cc = [100,0.0 ; 300,0.0 ; 500,0.0];
    genScat(Ns,Rc,Cc) in this case generates 20 randomly placed reflectors
    grouped into 3 clusters of 20 meters in diameter centered at (100,0), (300,0), and (500,0).
    """
    S = np.empty((sum(Ns),2))
    Nsum = [int(sum(Ns[:i])) for i in range(len(Ns)+1)]
    for i in range(len(Nsum)-1):
        S[Nsum[i]:Nsum[i+1],:] = genClust(Ns[i])*Rc[i]+np.repeat([Cc[i,:]],Ns[i], axis=0)
    return S


def genClust(N):
    """ genClust(N)
    Generates a cluster of N uniformly distributed positions on a
    unit diameter circle. Returns an array of N x 2 where each
    row is a position (x,y).
    """
    Clust = np.empty((N,2))
    n = 0
    while n < N:
        X = np.random.rand(2)-np.array([0.5,0.5])
        if X.dot(X) < 0.25:
            Clust[n,:]=X
            n = n + 1
    return Clust


def genDists(S, posTx, posRx):
    """ genDists(S,posTx,posRx)
    Receives an array of N x 2 where each row describes the
    position (x,y) of N reflectors and returns an array Dsts with N distances between
    posTx and posRx (vectors (x,y) describing positions of Tx and Rx)
    measured as straight lines connecting the points Tx, reflector, and Rx.
    Also returns an array D_ref_Rx with the N distances between reflector
    and Rx.
    By convention all distances are in meters.
    """

    Dsts = np.empty(S.shape[0])
    D_ref_Rx = np.empty(S.shape[0])
    for i in range(len(Dsts)):
        a = posTx - S[i,:]
        b = posRx - S[i,:]
        Dsts[i] = np.sqrt(a.dot(a)) + np.sqrt(b.dot(b))
        D_ref_Rx[i] = np.sqrt(b.dot(b))
    return Dsts, D_ref_Rx


def genhl(Dsts, fc, W, a_i, oversample=1, margin=0):

    """ genhl(Dsts, fc, W, a_i, oversample, margin)
    This function produces the discrete equivalent baseband impulse response
    of the channel corresponding to all paths with distances given by the
    vector Dsts, a central frequency fc, a bandwidth W, attenuations
    a_i (also a vector with the attenuations of each path).
    oversample is a parameter that must be an integer greater than or equal to 1 and
    is used to generate intermediate points between samples (to simulate
    the "analog" behavior of the channel).
    margin: the response is computed for floor(margin)/2 samples before the
    first received echo (or path) from the channel and likewise for the last received one.
    """

    if ((oversample-np.floor(oversample))!=0) | (oversample<1):
        raise ValueError('The oversample parameter must be an integer greater than or equal to 1.')

    c = 3e8                # m/s
    Rts = Dsts/c           # delays
    GroupRet = min(Rts)
    Td = max(Rts)-GroupRet # delay spread

    RtsRel = Rts - GroupRet

    hl = np.empty(int(np.floor(Td*W*oversample)+margin*oversample+1),dtype='complex128')
                                                        # h_l with l=0,1,...,floor(Td*W*oversample)+margin
    a_ib = a_i * np.exp(-1j*2*np.pi*fc*Rts)
    for l in range(len(hl)):
        hl[l] = (np.sinc(l/oversample - np.floor(margin/2) - RtsRel*W)).dot(a_ib.T)
    tt = np.arange(len(hl))/W/oversample - np.floor(margin/2)/W + GroupRet

    return hl, tt


def delaySpread(Dsts):
    """ delaySpread(Dsts)
    Receives a vector Dsts of distances (in meters) as a parameter
    and returns the delay spread Td (in seconds) between those distances.
    """
    Rts = Dsts/3e8
    return max(Rts)-min(Rts)

def DistRayleigh(x, s2):
    f = x * np.exp(-x**2 / (2 * s2)) / s2
    return f

def DistRician(x,s2,v):
    f = x*np.exp(-(x**2+v**2)/(2*s2))*np.i0(x*v/s2)/s2
    return f

# Raytracing attenuation model
def graf_sum(G, posTx, posRx, D, e):
    Dsts, D_ref_Rx = genDists(G,posTx,posRx)
    D_ref_Tx  = Dsts - D_ref_Rx
    DIST = [D_ref_Tx, D_ref_Rx]

# Analyzed attenuation model
def graf_mult(G, posTx, posRx, D, e):
    Dsts, D_ref_Rx = genDists(G,posTx,posRx)
    D_ref_Tx  = Dsts - D_ref_Rx
    DIST = [D_ref_Tx, D_ref_Rx]
