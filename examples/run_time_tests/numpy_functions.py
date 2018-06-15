import numpy as np

def numpy_chi2_v1(time, obs_flux, obs_flux_err, t_0, u_0, t_E):
    u = np.sqrt(np.square((time-t_0)/t_E) + u_0*u_0)
    u2 = np.square(u)
    magnification = (u2 + 2.) / (u * np.sqrt(u2 + 4.))
    fluxes = np.polyfit(magnification, obs_flux, 1, w=np.reciprocal(obs_flux_err))
    flux = fluxes[0] * magnification + fluxes[1]
    chi2 = np.sum(np.square((obs_flux - flux) / obs_flux_err))
    return chi2
