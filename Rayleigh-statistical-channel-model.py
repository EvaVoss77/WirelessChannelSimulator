from functions import *
from example import *
"""## Statistical Channel Model

To verify that the Rayleigh statistical model is satisfied, the bandwidth $ W_1 $ is used so that the channel exhibits flat fading behavior. N = 10,000 realizations were performed in the generated scenario, in which the position of the reflectors within the clusters was changed. For each realization, the absolute value of the central tap is saved, and a normalized histogram is created with these values. On the same histogram, a fit with the Rayleigh distribution is performed:

$ f(x) = \frac{x}{\sigma^2} e^{-\frac{x^2}{2\sigma^2}} $

In this fit, the parameter value of $ \sigma^2 = 27.70 $ was obtained.
"""

# Generate data to create a histogram
a_i = -1 * np.ones(np.size(Dsts))
st_rayleigh = []
N = 10000

for i in range(0, N):
    S = genScat(Ns, Rc, Cc)
    Dsts, _ = genDists(S, posTx, posRx)
    ha_1, ta_1 = genhl(Dsts, fc, W1, a_i, oversample, margin)
    ab = abs(ha_1)
    st_rayleigh.append(ab[140])

# Fit a Rayleigh function to the generated histogram
def DistRayleigh(x, s2):
    f = x * np.exp(-x**2 / (2 * s2)) / s2
    return f

# Parameters: s2, v
fig = plt.Figure()

bins = 40
c_rayleigh, b_rayleigh = np.histogram(st_rayleigh, bins)

A = sum(c_rayleigh) * (b_rayleigh[1] - b_rayleigh[0])
c_rayleigh = c_rayleigh / A

plt.hist(b_rayleigh[:-1], b_rayleigh, density=False, weights=c_rayleigh, color='#F2AB6D', edgecolor="black")
r1, c1 = opt.curve_fit(DistRayleigh, b_rayleigh[:bins], c_rayleigh)
aj = [DistRayleigh(i, r1[0]) for i in b_rayleigh]

plt.plot(b_rayleigh, aj)
plt.ylabel("Probability")
plt.xlabel("|h0|")

plt.show()

