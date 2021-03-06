import numpy as np
from astropy import units as u

from MulensModel.mulensobjects.mulenssystem import MulensSystem
from MulensModel.mulensobjects.lens import Lens
from MulensModel.mulensobjects.source import Source


def test_mulenssystem():
    kappa = 8.144183118384794 * u.mas / u.solMass
    lens = {'mass': 0.3 * u.solMass, 'dist': 4 * 10**3 * u.pc}
    source = {'dist' : 8 * 10**3 * u.pc}
    mu_rel = 3. * u.mas / u.yr
    pi_rel = (lens['dist'].to(u.mas, equivalencies=u.parallax()) 
              - source['dist'].to(u.mas, equivalencies=u.parallax()))
    thetaE = np.sqrt( kappa * lens['mass'] * pi_rel)
    tE = thetaE / mu_rel
    pi_E = pi_rel / thetaE

    test_system = MulensSystem(
        lens=Lens(mass=lens['mass'], distance=lens['dist']), 
        source=Source(distance=source['dist']),
        mu_rel=mu_rel)
    
    assert test_system.pi_rel == pi_rel
    assert abs(test_system.theta_E / thetaE - 1.) < 1.2e-4
    assert abs(test_system.pi_E / pi_E - 1.) < 1.2e-4
    assert isinstance(test_system.pi_E, float)
    assert abs(test_system.t_E / tE - 1.) < 1.2e-4

def test_mulenssytem():
    lens = Lens(mass=0.64, distance=4.0)
    source = Source(distance=8.0)
    system = MulensSystem(lens=lens, source=source)

    assert abs(system.theta_E.value / 0.807177 - 1.) < 1.2e-4
    assert abs(system.r_E.value / 3.228708 - 1.) < 1.2e-4
    assert abs(system.r_E_tilde.value / 6.457416 - 1.) < 1.2e-4

