import numpy as np
from numpy_functions import numpy_chi2_v1


MAG_ZEROPOINT = 18.

file_1 = "test_1000.txt"
data_1 = np.loadtxt(file_1, unpack=True)
time = data_1[0]
obs_flux = np.power(10., -0.4 * (data_1[1] - MAG_ZEROPOINT))
obs_flux_err = data_1[2] * obs_flux * 0.4 * np.log(10.)

t_0 = 5379.57091
u_0 = 0.52298
t_E = 17.94002
