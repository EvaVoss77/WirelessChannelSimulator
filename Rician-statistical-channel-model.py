from functions import *
from example import *
"""## Statistical Channel Model

To verify the statistical model of Rician, the same scenario is used with flat fading behavior of the channel. For this, the attenuation vector is artificially modified so that there is a specular path whose energy is K times the energy of the sum of the other paths. For values of K = 100, 200, 300, 400, 10,000 realizations are generated with which histograms are created. A fit is made with the Rician distribution for each of these values:

$ f(x) = \frac{x}{\sigma^2} e^{-\frac{(x^2+\nu^2)}{2\sigma^2}} I_0\left(\frac{x\nu}{\sigma^2}\right) $

The fitting curves of each histogram are compared. It is observed that as the value of K increases, the data distribution becomes increasingly selective. This warns us that the greater the difference in energy of the specular path with higher energy compared to the other paths, the greater the probability that the channel's impulse response will correspond to this path. That is, the channel will tend towards deterministic behavior if there is a path whose energy is much greater than that of the other paths.
"""

#Genero distintos escenarios
Wc = 1.023*1e6
W1 = 0.1*Wc
N = 5000
K = 4       #Factor

#Camino especular
a_i = -1*np.ones(np.size(Dsts))
a_i = a_i/np.sqrt((-1*(sum(a_i)+1)*K))
ran = np.random.randint(0,len(a_i))    #posicion del camino especular
a_i[ran] = -1

st_rician = []

for i in range(0,N):
    S = genScat(Ns,Rc,Cc)
    Dsts,_ = genDists(S,posTx,posRx)
    ha_1, ta_1 = genhl(Dsts, fc, W1, a_i, oversample, margin)
    ab = abs(ha_1)
    st_rician.append(ab[140])

a_i = -1*np.ones(np.size(Dsts))
a_i = a_i/np.sqrt((-1*(sum(a_i)+1)*K))
ran = np.random.randint(0,len(a_i))    #posicion del camino especular
a_i[ran] = -1

# Fit a Rician function to the generated histogram
def DistRician(x,s2,v):
    f = x*np.exp(-(x**2+v**2)/(2*s2))*np.i0(x*v/s2)/s2
    return f

bins = 40
C_rician = plt.hist(st_rician, bins, density=True, color='#F2AB6D', edgecolor = "black")

r2, c2 = opt.curve_fit(DistRician, C_rician[1][:bins], C_rician[0])
aj = [DistRician(i, r2[0], r2[1]) for i in C_rician[1][:bins]]

plt.plot(C_rician[1][:bins],aj)
plt.ylabel("Probabilidad")
plt.xlabel("|h0|")