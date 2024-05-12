from functions import *
from example import *

"""# Channel Behavior

Simulation of a channel, where the transmitter and the receiver are separated by a fixed distance of 500 m. There are three clusters in which 20 reflectors are distributed within a 15 m diameter. For this channel, the coherence bandwidth was estimated considering the worst possible case in which the paths maintain the maximum possible distance between them. From these paths, the Delay Spread was determined, with which the coherence bandwidth was calculated resulting in: $Wc = 1.023 MHz$.

Three bandwidths $ W_1 < W_2 < W_3 $ were proposed such that:

1. All the channel information is concentrated in a single "tap."
2. The input/output system can resolve the clusters but not the paths that make them up.
3. The input/output system can resolve a good portion of the paths.

"""
margin = 15
oversample = 20

# Estimation
Wc = 1.023 * 1e6

'''1) All channel information is contained in a single tap
To achieve the conditions of the first case, the channel must be in flat fading condition
for which W << Wc. For this case, the chosen value for the communication bandwidth was
W1 = 0.1Wc = 102.3 kHz.
'''
W1 = 0.1 * Wc

# Temporal domain response
ha_1, ta_1 = genhl(Dsts, fc, W1, a_i, oversample, margin)
hd_1, td_1 = genhl(Dsts, fc, W1, a_i, 1, margin)
# Frequency domain response
Ha_1 = np.fft.fftshift(np.fft.fft(ha_1))
fa_1 = np.fft.fftshift(np.fft.fftfreq(ta_1.size, abs(ta_1[1] - ta_1[0])))

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(ta_1 * 1e6, abs(ha_1) ** 2, linewidth=1, label="Analog")
plt.stem(td_1 * 1e6, abs(hd_1) ** 2, 'r', label="Digital")
plt.xlabel('time [$\mu$s]')
plt.ylabel('$|h|$')
plt.title('Temporal domain response for $W_1 = 0.1W_c$')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(fa_1 / 1e9, abs(Ha_1) ** 2, linewidth=1, label='W1 = ' + str(float(W1 / 1e6)) + ' MHz')
plt.xlabel('frequency [GHz]')
plt.ylabel('$|H|^2$')
plt.title('Frequency domain responses for $W_1 = 0.1W_c$')
plt.legend()

plt.tight_layout()
plt.show()

''' 2) The system can resolve the clusters but not the paths that make them up
In the second case mentioned, in order to resolve the clusters, the frequency-selective condition must be met
for which W > Wc, however, a frequency must be chosen such that it does not resolve
the reflectors so it should not be too high. For this case, a bandwidth of W1 = 15Wc = 15.35MHz was chosen.
'''
W2 = 15 * Wc

# Temporal domain response
ha_2, ta_2 = genhl(Dsts, fc, W2, a_i, oversample, margin)
hd_2, td_2 = genhl(Dsts, fc, W2, a_i, 1, margin)
# Frequency domain response
Ha_2 = np.fft.fftshift(np.fft.fft(ha_2))
fa_2 = np.fft.fftshift(np.fft.fftfreq(ta_2.size, abs(ta_2[1] - ta_2[0])))

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(ta_2 * 1e6, abs(ha_2) ** 2, linewidth=1, label="Analog")
plt.stem(td_2 * 1e6, abs(hd_2) ** 2, 'r', label="Digital")
plt.xlabel('time [$\mu$s]')
plt.ylabel('$|h|$')
plt.title('Temporal domain response for $W_2 = 15W_c$')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(fa_2 / 1e9, abs(Ha_2) ** 2, linewidth=1, label='W2 = ' + str(int(W2 / 1e6)) + ' MHz')
plt.xlabel('frequency [GHz]')
plt.ylabel('$|H|^2$')
plt.title('Frequency domain responses for $W_2 = 15W_c$')
plt.legend()

plt.tight_layout()
plt.show()

''' 3) The system can resolve a good portion of the paths that make them up
For the third case, the frequency-selective condition must be met to resolve the reflectors,
for this, a bandwidth of W3 = 100Wc = 102.3MHz was used.
'''
W3 = 100 * Wc

# Temporal domain response
ha_3, ta_3 = genhl(Dsts, fc, W3, a_i, oversample, margin)
hd_3, td_3 = genhl(Dsts, fc, W3, a_i, 1, margin)
# Frequency domain response
Ha_3 = np.fft.fftshift(np.fft.fft(ha_3))
fa_3 = np.fft.fftshift(np.fft.fftfreq(ta_3.size, abs(ta_3[1] - ta_3[0])))

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(ta_3 * 1e6, abs(ha_3) ** 2, linewidth=1, label="Analog")
plt.stem(td_3 * 1e6, abs(hd_3) ** 2, 'r', label="Digital")
plt.xlabel('time [$\mu$s]')
plt.ylabel('$|h|$')
plt.title('Temporal domain response for $W_3 = 100W_c$')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(fa_3 / 1e9, abs(Ha_3) ** 2, linewidth=1, label='W2 = ' + str(int(W3 / 1e6)) + ' MHz')
plt.xlabel('frequency [GHz]')
plt.ylabel('$|H|^2$')
plt.title('Frequency domain responses for $W_3 = 100W_c$')
plt.legend()

plt.tight_layout()
plt.show()