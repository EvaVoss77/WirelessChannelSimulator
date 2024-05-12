from functions import *
from example import *

# Measurements of intensity are performed at the first "tap" of the channel for different points in an X-Y region of space (moving the Rx and keeping the Tx fixed)
Wc = 1.023 * 1e6
W1 = 0.1 * Wc
oversample = 20
a_i = -1 * np.ones(np.size(Dsts))
margin = 15
N = 50
M = 50
posTx = np.array([-50, 0])
posRx = np.array([500, 0])

mapa = np.zeros((N, M))
S = genScat(Ns, Rc, Cc)
for y in range(0, N):
    aux = np.zeros(0)
    for x in range(0, M):
        posRx = [x * 0.01, y * 0.01]
        Dsts, _ = genDists(S, posTx, posRx)
        ha_1, ta_1 = genhl(Dsts, fc, W1, a_i, oversample, margin)
        ab = abs(ha_1) ** 2
        aux = np.append(aux, ab[140])
    mapa[:, y] = aux

    i = 0
    for s in G:
        if ((DIST[0][i] + DIST[1][i]) > D and (DIST[0][i] + DIST[1][i]) < D + e):
            plt.plot(s[0], s[1], 'yo')
        else:
            plt.plot(s[0], s[1], 'b.', markersize=2)
        i = i + 1
    plt.plot(posTx[0], posTx[1], 'go')
    plt.plot(posRx[0], posRx[1], 'ro')

    i = 0
    for s in G:
        if ((DIST[0][i] * DIST[1][i]) >= D and (DIST[0][i] * DIST[1][i]) <= D + e):
            plt.plot(s[0], s[1], 'yo')
        else:
            plt.plot(s[0], s[1], 'b.', markersize=2)
        i = i + 1
    plt.plot(posTx[0], posTx[1], 'go')
    plt.plot(posRx[0], posRx[1], 'ro')


Ns = np.array([10000])  # number of reflectors per cluster
Rc = np.array([2000])  # cluster diameter in meters
Cc = np.array([[0, 0]])
posTx = np.array([-500, 0])
G = genScat(Ns, Rc, Cc)
D = 850
e = 50

# Raytracing attenuation model
for i in range(0, 7):
    # The receiver moves linearly in the x-axis direction
    posRx = np.array([-400 + i * 100, 0.0])
    plt.figure()
    # A plot of the receiver's movement in the x and y coordinates is generated, marking in yellow the reflectors for which the same attenuation is generated
    graf_sum(G, posTx, posRx, D, e)
    plt.axis('equal')
    plt.title("d1+d2 : " + str(i))
    plt.xlabel("x[m]")
    plt.ylabel("y[m]")

D = 100000
e = 10000

# Analyzed attenuation model
for i in range(0, 5):
    # The receiver moves linearly in the x-axis direction
    posRx = np.array([-400 + i * 200, 0.0])
    plt.figure()
    graf_mult(G, posTx, posRx, D, e)
    plt.axis('equal')
    plt.title("d1*d2 : " + str(i))
    plt.xlabel("x[m]")
    plt.ylabel("y[m]")
