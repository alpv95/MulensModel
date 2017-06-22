import numpy as np

from MulensModel.magnificationcurve import MagnificationCurve
from MulensModel.modelparameters import ModelParameters


def test_fspl_noLD():
    """check if FSPL magnification is calculate properly"""
    t_0 = 2456789.012345
    t_E = 23.4567
    u_0 = 1e-4
    rho = 1e-3
    t_vec = np.array([-(rho**2-u_0**2)**0.5, 0., ((0.5*rho)**2-u_0**2)**0.5])
    t_vec = t_vec * t_E + t_0
    
    params = ModelParameters(t_0=t_0, u_0=u_0, t_E=t_E, rho=rho)

    mag_curve = MagnificationCurve(times=t_vec, parameters=params)
    methods = [t_0-t_E, 'finite_source_Gould94', t_0+t_E]
    mag_curve.set_magnification_methods(methods, 'point_source')
    results = mag_curve.get_point_lens_magnification()
    
    u = np.array([rho, u_0, 0.5*rho])
    pspl = (u**2 + 2.) / np.sqrt(u**2 * (u**2 + 4.))
    expected = np.array([1.27323965, 0.19949906, 0.93421546]) # These values 
    # were calculated by Andy Gould (file b0b1.dat).
    expected *= pspl
    
    np.testing.assert_almost_equal(expected, results, decimal=5)
    
def test_fspl():
    """check if FSPL magnification is calculate properly"""
    t_0 = 2456789.012345
    t_E = 23.4567
    u_0 = 1e-4
    rho = 1e-3
    t_vec = np.array([-(rho**2-u_0**2)**0.5, 0., ((0.5*rho)**2-u_0**2)**0.5])
    t_vec = t_vec * t_E + t_0
    
    params = ModelParameters(t_0=t_0, u_0=u_0, t_E=t_E, rho=rho)

    mag_curve = MagnificationCurve(times=t_vec, parameters=params)
    methods = [t_0-t_E, 'finite_source_LD_Gould94', t_0+t_E]
    mag_curve.set_magnification_methods(methods, 'point_source')
    results = mag_curve.get_point_lens_magnification()
    
    u = np.array([rho, u_0, 0.5*rho])
    pspl = (u**2 + 2.) / np.sqrt(u**2 * (u**2 + 4.))
    expected = np.array([1.27323965, 0.19949906, 0.93421546]) # These values 
    # were calculated by Andy Gould (file b0b1.dat).
    expected *= pspl
    
    np.testing.assert_almost_equal(expected, results, decimal=5)    
    