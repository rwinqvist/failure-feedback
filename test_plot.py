import matplotlib.pyplot as plt
import numpy as np

plt.switch_backend('TkAgg')


t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2*np.pi*t)
print("plotting")
plt.plot(t, s)
print("not plotting")

plt.title('About as simple as it gets, folks')
plt.show()