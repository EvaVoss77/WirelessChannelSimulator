from functions import *
from example import *

"""## Cohernce Distance

In the same scenario as before, with a flat fading channel, a map of the amplitude strength of the main tap $ h_0 $ is created by varying the position of the receiver in a region of 2m x 2m at a distance of $d = 400 $ m from the transmitter. The result shows regions where the channel energy is higher. The coherence distance was estimated from the distance between the lines of greatest intensity, giving a value of $ d_c = 27 $ cm.
"""

# Intensity measurements of the first "tap" of the channel are performed for different
# points in an X-Y region of space (moving the Rx while keeping the Tx fixed)
Wc = 1.023 * 1e6
W1 = 0.1 * Wc
oversample = 20
a_i = -1 * np.ones(np.size(Dsts))
margin = 15
N = 50
M = 50

mapa = np.zeros((N, M))
S = genScat(Ns, Rc, Cc)
for y in range(0, N):
    aux = np.zeros(0)
    for x in range(0, M):
        posRx = [x * 0.1, y * 0.1]
        Dsts, _ = genDists(S, posTx, posRx)
        ha_1, ta_1 = genhl(Dsts, fc, W1, a_i, oversample, margin)
        ab = abs(ha_1) ** 2
        aux = np.append(aux, ab[140])
    mapa[:, y] = aux

plt.imshow(mapa, cmap='cool', interpolation='nearest')
plt.show()