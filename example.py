from functions import *
"""Example
Three clusters with 20 reflectors each
"""

Ns = np.array([20, 20, 20])  # Number of reflectors per cluster
Rc = np.array([15, 15, 15])  # Diameter of clusters in meters
Cc = np.array([[-50.0, 250.0], [150, 250.0], [200, 250.0]])  # Cluster centers
posTx = np.array([0, 0])
posRx = np.array([0.0, 500.0])
fc = 1e9  # Frequency [Hz]
c = 300e6  # Speed of light [m/s]
vmax = 60000 / 3600  # Maximum speed [m/s]
K = 0.0  # K-factor

# Generate clusters and respective distances/attenuations
S = genScat(Ns, Rc, Cc)
Dsts, _ = genDists(S, posTx, posRx)
a_i = -1 * np.ones(np.size(Dsts))

# Generate two impulse responses (for different bandwidths)
# ha_i --> "analog" responses (emulated using 10 times oversample)
# hd_i --> digital responses (no oversample)
# ta_i and td_i are the time instants for each response value
margin = 15
oversample = 20
ha_1, ta_1 = genhl(Dsts, fc, 20.0 / delaySpread(Dsts), a_i, oversample, margin)  # W = 20/Td  ===>  Ts = Td/20
hd_1, td_1 = genhl(Dsts, fc, 20.0 / delaySpread(Dsts), a_i, 1, margin)
ha_2, ta_2 = genhl(Dsts, fc, 200.0 / delaySpread(Dsts), a_i, oversample, margin)
hd_2, td_2 = genhl(Dsts, fc, 200.0 / delaySpread(Dsts), a_i, 1, margin)

plt.figure(1)
plt.plot(ta_1 * 1e6, abs(ha_1) ** 2, linewidth=1)
plt.stem(td_1 * 1e6, abs(hd_1) ** 2, 'r')
plt.xlabel('time [$\mu$s]')
plt.ylabel('$|h|$')
plt.title('Analog (blue) and Digital (red) Responses')

plt.figure(2)
plt.plot(ta_2 * 1e6, abs(ha_2) ** 2, linewidth=1)
plt.stem(td_2 * 1e6, abs(hd_2) ** 2, 'r')
plt.xlabel('time [$\mu$s]')
plt.ylabel('$|h|$')
plt.title('Analog (blue) and Digital (red) Responses')

plt.figure(3)
for s in S:
    plt.plot(s[0], s[1], 'b.')
plt.plot(posTx[0], posTx[1], 'go')
plt.plot(posRx[0], posRx[1], 'ro')
plt.axis('equal')
plt.title('Cluster Map')