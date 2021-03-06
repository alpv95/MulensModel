import numpy as np
import unittest
from astropy import units as u

from MulensModel import Model, ModelParameters, MulensData, Caustics


def test_n_lenses():
    """check n_lenses property"""
    model_1 = Model({"t_0": 2456789., "u_0": 1., "t_E": 30.})
    model_2 = Model({"t_0": 2456789., "u_0": 1., "t_E": 30.,
        "s": 1.1234, "q": 0.123, 'alpha': 12.34})
    assert model_1.n_lenses == 1
    assert model_2.n_lenses == 2

# Point Lens Tests
def test_model_PSPL_1():
    """tests basic evaluation of Paczynski model"""
    t_0 = 5379.57091
    u_0 = 0.52298
    t_E = 17.94002
    times = np.array([t_0-2.5*t_E, t_0, t_0+t_E])
    data = MulensData(data_list=[times, times*0., times*0.])
    model = Model({'t_0':t_0, 'u_0':u_0, 't_E':t_E})
    model.parameters.u_0 = u_0
    model.parameters.t_E = t_E
    model.set_datasets([data])
    np.testing.assert_almost_equal(model.data_magnification, [
            np.array([1.028720763, 2.10290259, 1.26317278])], 
            err_msg="PSPL model returns wrong values")

def test_model_init_1():
    """tests if basic parameters of Model.__init__() are properly passed"""
    t_0 = 5432.10987
    u_0 = 0.001
    t_E = 123.456
    rho = 0.0123
    my_model = Model({'t_0':t_0, 'u_0':u_0, 't_E':t_E, 'rho':rho})
    np.testing.assert_almost_equal(my_model.parameters.t_0, t_0, err_msg='t_0 not set properly')
    np.testing.assert_almost_equal(my_model.parameters.u_0, u_0, err_msg='u_0 not set properly')
    np.testing.assert_almost_equal(my_model.parameters.t_E, t_E, err_msg='t_E not set properly')
    np.testing.assert_almost_equal(my_model.parameters.rho, rho, err_msg='rho not set properly')

class TestModel(unittest.TestCase):
    def test_negative_t_E(self):
        with self.assertRaises(ValueError):
            my_model = Model({'t_0':2450000., 'u_0':0.1, 't_E':-100.})

def test_model_parallax_definition():
    # JCY: I don't think we should allow parameters to be set sequentially like this.
    #model_1 = Model()
    #model_1.parameters.pi_E = [0.1, 0.2]
    #assert model_1.pi_E_N == 0.1
    #assert model_1.pi_E_E == 0.2

    # JCY: below is acceptable (i.e. if the parameter has been
    # defined, the user can change it. If the user wants to add a
    # parameter, they need to create a new model.)
    model_2 = Model({'t_0':2450000., 'u_0':0.1, 't_E':100., 'pi_E_N':0.1, 'pi_E_E':0.2})

    model_2.parameters.pi_E_N = 0.3
    model_2.parameters.pi_E_E = 0.4
    assert model_2.parameters.pi_E_N == 0.3
    assert model_2.parameters.pi_E_E == 0.4

    model_3 = Model({'t_0':2450000., 'u_0':0.1, 't_E':100., 'pi_E':(0.5, 0.6)})
    assert model_3.parameters.pi_E_N == 0.5
    assert model_3.parameters.pi_E_E == 0.6

    model_4 = Model({'t_0':2450000., 'u_0':0.1, 't_E':100., 'pi_E_N':0.7, 'pi_E_E':0.8})
    assert model_4.parameters.pi_E_N == 0.7
    assert model_4.parameters.pi_E_E == 0.8

def test_coords_transformation():
    """this was tested using http://ned.ipac.caltech.edu/forms/calculator.html"""
    coords = "17:54:32.1 -30:12:34.0"
    model = Model({'t_0':2450000., 'u_0':0.1, 't_E':100.}, coords=coords)

    np.testing.assert_almost_equal(model.coords.galactic_l.value, 359.90100049-360., decimal=4)
    np.testing.assert_almost_equal(model.coords.galactic_b.value, -2.31694073, decimal=3)

    np.testing.assert_almost_equal(model.coords.ecliptic_lon.value, 268.81102051, decimal=1)
    np.testing.assert_almost_equal(model.coords.ecliptic_lat.value, -6.77579203, decimal=2)


def test_init_parameters():
    """are parameters properly passed between Model and ModelParameters?"""
    t_0 = 6141.593
    u_0 = 0.5425
    t_E = 62.63*u.day
    params = ModelParameters({'t_0':t_0, 'u_0':u_0, 't_E':t_E})
    model = Model(parameters=params)
    np.testing.assert_almost_equal(model.parameters.t_0, t_0)
    np.testing.assert_almost_equal(model.parameters.u_0, u_0)
    np.testing.assert_almost_equal(model.parameters.t_E, t_E.value)

def test_limb_darkening():
    """check if limb_darkening coeffs are properly passed and converted"""
    gamma = 0.4555
    u = 3. * gamma / (2. + gamma)

    model = Model({'t_0':2450000., 'u_0':0.1, 't_E':100., 'rho':0.001})
    model.set_limb_coeff_gamma('I', gamma)

    np.testing.assert_almost_equal(model.get_limb_coeff_gamma('I'), gamma)
    np.testing.assert_almost_equal(model.get_limb_coeff_u('I'), u)

def test_t_E():
    """make sure t_E can be accessed properly"""
    t_0 = 2460000.
    u_0 = 0.1
    t_E = 12.3456
    t_star = 0.01234
    params = dict(t_0=t_0, u_0=u_0, t_E=t_E)
    model_1 = Model(params)
    params['t_star'] = t_star
    model_2 = Model(params)

    np.testing.assert_almost_equal(model_1.parameters.t_E, t_E)
    np.testing.assert_almost_equal(model_2.parameters.t_E, t_E)

# Binary Lens tests
# Binary lens parameters:
alpha = 229.58 * u.deg
s = 1.3500 
q = 0.00578
# Other parameters
t_E = 62.63 * u.day
rho = 0.01

# Adjust t_0, u_0 from primary to CM
shift_x = -s * q / (1. + q)
delta_t_0 = -t_E.value * shift_x * np.cos(alpha).value
delta_u_0 = -shift_x * np.sin(alpha).value
t_0 = 2456141.593 + delta_t_0
u_0 = 0.5425 + delta_u_0

def test_BLPS_01():
    """simple binary lens with point source"""
    params = ModelParameters({
            't_0': t_0, 'u_0': u_0, 't_E': t_E, 'alpha': alpha, 's': s, 
            'q': q})

    model = Model(parameters=params)
    t = np.array([2456112.5])
    data = MulensData(data_list=[t, t*0.+16., t*0.+0.01])
    model.set_datasets([data])
    magnification = model.data_magnification[0][0]
    np.testing.assert_almost_equal(magnification, 4.691830781584699) # This value comes from early version of this code.
    # np.testing.assert_almost_equal(m, 4.710563917) # This value comes from Andy's getbinp().

def test_BLPS_02():
    """simple binary lens with extended source and different methods to
    evaluate magnification"""

    params = ModelParameters({
            't_0': t_0, 'u_0': u_0, 't_E': t_E, 'alpha': alpha, 's': s, 
            'q': q, 'rho': rho})
    model = Model(parameters=params)

    t = (np.array([6112.5, 6113., 6114., 6115., 6116., 6117., 6118., 6119]) + 
        2450000.)
    methods = [2456113.5, 'Quadrupole', 2456114.5, 'Hexadecapole', 2456116.5, 
        'VBBL', 2456117.5]
    model.set_magnification_methods(methods)

    data = MulensData(data_list=[t, t*0.+16., t*0.+0.01])
    model.set_datasets([data])
    result = model.data_magnification[0]

    expected = np.array([4.69183078, 2.87659723, 1.83733975, 1.63865704, 
        1.61038135, 1.63603122, 1.69045492, 1.77012807])
    np.testing.assert_almost_equal(result, expected)

    # Below we test passing the limb coeff to VBBL function.
    data.bandpass = 'I'
    model.set_limb_coeff_u('I', 10.) # This is an absurd value but I needed something quick.
    result = model.data_magnification[0]
    np.testing.assert_almost_equal(result[5], 1.6366862)

def test_BLPS_02_AC():
    """
    simple binary lens with extended source and different methods to evaluate magnification
    - version with adaptivecontouring
    """
    params = ModelParameters({
            't_0': t_0, 'u_0': u_0, 't_E': t_E, 'alpha': alpha, 's': s, 
            'q': q, 'rho': rho})
    model = Model(parameters=params)

    t = (np.array([6112.5, 6113., 6114., 6115., 6116., 6117., 6118., 6119]) + 
        2450000.)
    ac_name = 'Adaptive_Contouring'
    methods = [2456113.5, 'Quadrupole', 2456114.5, 'Hexadecapole', 2456116.5, 
        ac_name, 2456117.5]
    accuracy_1 = {'accuracy': 0.04}
    accuracy_2 = {'accuracy': 0.01, 'ld_accuracy': 0.00001}
    model.set_magnification_methods(methods)
    model.set_magnification_methods_parameters({ac_name: accuracy_1})

    data = MulensData(data_list=[t, t*0.+16., t*0.+0.01])
    model.set_datasets([data])
    result = model.data_magnification[0]

    expected = np.array([4.69183078, 2.87659723, 1.83733975, 1.63865704, 
        1.61038135, 1.63603122, 1.69045492, 1.77012807])
    np.testing.assert_almost_equal(result, expected, decimal=3) 

    # Below we test passing the limb coeff to VBBL function.
    data.bandpass = 'I'
    model.set_limb_coeff_u('I', 10.) # This is an absurd value but I needed something quick.
    model.set_magnification_methods_parameters({ac_name: accuracy_2})
    result = model.data_magnification[0]
    np.testing.assert_almost_equal(result[5], 1.6366862, decimal=3) 

def test_methods_parameters():
    """make sure additional parameters are properly passed to very inner functions"""
    params = ModelParameters({
            't_0': t_0, 'u_0': u_0, 't_E': t_E, 'alpha': alpha, 's': s, 
            'q': q, 'rho': rho})
    model = Model(parameters=params)

    t = np.array([2456117.])
    methods = [2456113.5, 'Quadrupole', 2456114.5, 'Hexadecapole', 2456116.5, 
        'VBBL', 2456117.5]
    model.set_magnification_methods(methods)

    data = MulensData(data_list=[t, t*0.+16., t*0.+0.01])
    model.set_datasets([data])
    result_1 = model.data_magnification[0]

    vbbl_options = {'accuracy': 0.1}
    methods_parameters = {'VBBL': vbbl_options}
    model.set_magnification_methods_parameters(methods_parameters)
    result_2 = model.data_magnification[0]

    vbbl_options = {'accuracy': 1.e-5}
    methods_parameters = {'VBBL': vbbl_options}
    model.set_magnification_methods_parameters(methods_parameters)
    result_3 = model.data_magnification[0]

    assert result_1[0] != result_2[0]
    assert result_1[0] != result_3[0]
    assert result_2[0] != result_3[0]

def test_caustic_for_orbital_motion():
    """
    check if caustics calculated for different epochs in orbital motion model
    are as expected
    """
    q = 0.1
    s = 1.3
    model = Model(parameters={'t_0': 100., 'u_0': 0.1, 't_E': 10., 'q': q,
        's': s, 'ds_dt': 0.5, 'alpha': 0., 'dalpha_dt': 0.})

    model.update_caustics()
    np.testing.assert_almost_equal(model.caustics.get_caustics(), 
        Caustics(q=q, s=s).get_caustics())

    model.update_caustics(100.+365.25/2)
    np.testing.assert_almost_equal(model.caustics.get_caustics(), 
        Caustics(q=q, s=1.55).get_caustics())

def test_magnifications_for_orbital_motion():
    """
    make sure that orbital motion parameters are properly passed to 
    magnification methods calculations
    """
    dict_static = {'t_0': 100., 'u_0': 0.1, 't_E': 100., 'q': 0.99,
        's': 1.1, 'alpha': 10.}
    dict_motion = dict_static.copy()
    dict_motion.update({'ds_dt': -2, 'dalpha_dt': -300.})
    static = Model(dict_static)
    motion = Model(dict_motion)

    t_1 = 100.
    np.testing.assert_almost_equal(
        static.magnification(t_1), 
        motion.magnification(t_1))

    t_2 = 130.
    static.parameters.s = 0.93572895
    static.parameters.alpha = 345.359342916
    np.testing.assert_almost_equal(
        static.magnification(t_2),
        motion.magnification(t_2))

def test_model_binary_and_finite_sources():
    """
    test if model magnification calculation for binary source works with 
    finite sources (both rho and t_star given)
    """
    model = Model({
        't_0_1': 5000., 'u_0_1': 0.005, 'rho_1': 0.001,
        't_0_2': 5100., 'u_0_2': 0.0003, 't_star_2': 0.03, 't_E': 25.})
    model_1 = Model(model.parameters.source_1_parameters)
    model_2 = Model(model.parameters.source_2_parameters)

    t1 = 4999.95
    t2 = 5000.05
    t3 = 5099.95
    t4 = 5100.05
    finite = 'finite_source_uniform_Gould94'
    model.set_magnification_methods([t1, finite, t2, 'point_source', t3,
        finite, t4])
    model_1.set_magnification_methods([t1, finite, t2])
    model_2.set_magnification_methods([t3, finite, t4])

    # prepare fake data:
    (f_s_1, f_s_2, f_b) = (100., 300., 50.)
    time = np.linspace(4900., 5200, 4200.)
    mag_1 = model_1.magnification(time)
    mag_2 = model_2.magnification(time)
    flux = f_s_1 * mag_1 + f_s_2 * mag_2 + f_b
    data = MulensData(data_list=[time, flux, 1.+0.*time], phot_fmt='flux')
    model.set_datasets([data])
    model_1.set_datasets([data])
    model_2.set_datasets([data])
    
    fitted = model.get_data_magnification(data)
    expected = (mag_1 * f_s_1 + mag_2 * f_s_2) / (f_s_1 + f_s_2)
    np.testing.assert_almost_equal(fitted, expected)
