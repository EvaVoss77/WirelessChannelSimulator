The work consisted of analyzing the numerical simulation of a wireless channel for different scenarios, varying the cluster diameter and the number of reflectors. The first step was to classify the channels for different bandwidths and estimate the coherence bandwidth from this. Afterward, the Rayleigh and Rician statistical models were verified. Finally, a force map was created to estimate the coherence distance.

# **Numerical Simulation of the Wireless Channel (CI) as shown in the figure.**

The data to consider for the simulations are:

- The carrier frequency fc is 1 GHz.
- The distance between the transmitter and the receiver (Tx and Rx in Fig. 1, respectively) is on the order of kilometers.
- The distance between "clusters" (d3 in Fig. 1) is on the order of hundreds of meters.
- The diameter of the "clusters" (d2 in Fig. 1) is on the order of tens of meters.
- The average distance between reflectors or "scatterers" (d1 in Fig. 1) is on the order of meters.

![int](https://github.com/EvaVoss77/WirelessChannelSimulator/assets/126124561/cd72bfe1-a2f6-43a0-bbdc-10a37085a3b7)

# Channel Behavior

Simulation of a channel, where the transmitter and the receiver are separated by a fixed distance of 500 m. There are three clusters in which 20 reflectors are distributed within a 15 m diameter. For this channel, the coherence bandwidth was estimated considering the worst possible case in which the paths maintain the maximum possible distance between them. From these paths, the Delay Spread was determined, with which the coherence bandwidth was calculated resulting in: $Wc = 1.023 MHz$.

Three bandwidths $W_1 < W_2 < W_3$ were proposed such that:

1. All the channel information is concentrated in a single "tap": To achieve the conditions of the first case, the channel must be in flat fading condition for which $W << W_c$. For this case, the chosen value for the communication bandwidth was $W1 = 0.1W_c = 102.3$ kHz.
2. The input/output system can resolve the clusters but not the paths that make them up: In the second case mentioned, in order to resolve the clusters, the frequency-selective condition must be met for which $W > W_c$, however, a frequency must be chosen such that it does not resolve the reflectors so it should not be too high. For this case, a bandwidth of W1 = 15Wc = 15.35MHz was chosen.
3. The input/output system can resolve a good portion of the paths: For the third case, the frequency-selective condition must be met to resolve the reflectors, for this, a bandwidth of W3 = 100Wc = 102.3MHz was used

## Statistical Channel Model

To verify that the Rayleigh statistical model is satisfied, the bandwidth $W_1$ is used so that the channel exhibits flat fading behavior. $N = 10,000$ realizations were performed in the generated scenario, in which the position of the reflectors within the clusters was changed. For each realization, the absolute value of the central tap is saved, and a normalized histogram is created with these values. On the same histogram, a fit with the Rayleigh distribution is performed:

$$ f(x) = \frac{x}{\sigma^2} e^{-\frac{x^2}{2\sigma^2}} $$

In this fit, the parameter value of $\sigma^2 = 27.70$ was obtained.

To verify the statistical model of Rician, the same scenario is used with flat fading behavior of the channel. For this, the attenuation vector is artificially modified so that there is a specular path whose energy is K times the energy of the sum of the other paths. For values of $K = 100, 200, 300, 400$ realizations are generated with which histograms are created. A fit is made with the Rician distribution for each of these values:

$$ f(x) = \frac{x}{\sigma^2} e^{-\frac{(x^2+\nu^2)}{2\sigma^2}} I_0\left(\frac{x\nu}{\sigma^2}\right) $$

The fitting curves of each histogram are compared. It is observed that as the value of K increases, the data distribution becomes increasingly selective. This warns us that the greater the difference in energy of the specular path with higher energy compared to the other paths, the greater the probability that the channel's impulse response will correspond to this path. That is, the channel will tend towards deterministic behavior if there is a path whose energy is much greater than that of the other paths.

## Cohernce Distance

In the same scenario as before, with a flat fading channel, a map of the amplitude strength of the main tap $h_0$ is created by varying the position of the receiver in a region of 2m x 2m at a distance of $d = 400$ m from the transmitter. The result shows regions where the channel energy is higher. The coherence distance was estimated from the distance between the lines of greatest intensity, giving a value of $d_c = 27$ cm.
