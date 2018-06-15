"""
Run benchmarks using perf package. We run the same calculations using
MulensModel, pyLIMA, and numpy.
"""
import perf


def read_and_simplify(file_name):
    """
    Read file and combine it in a single line.
    """
    with open(file_name) as in_file:
        lines = [line for line in in_file.readlines() if line.rstrip()]
        text = ''.join(lines).replace('\n', '; ')
    return text


kwargses = []
# Add settings for simple PSPL models:
kwargses.append(dict(name='MM', setup=read_and_simplify('MM_setup_1.py'), 
    stmt='event.get_chi2()'))
kwargses.append(dict(name='pyLIMA', 
    setup=read_and_simplify('pyLIMA_setup_1.py'), 
    stmt='chi2_telescope(your_event, model_1, parameters_list)'))
kwargses.append(dict(name='numpy', 
    setup=read_and_simplify('numpy_setup_1.py'),
    stmt='numpy_chi2_v1(time, obs_flux, obs_flux_err, t_0, u_0, t_E)'))

# Add settings for PSPL models with parallax:
kwargses.append(dict(name='MM_piE', setup=read_and_simplify('MM_setup_2.py'), 
    stmt='event.get_chi2()'))
kwargses.append(dict(name='pyLIMA_piE', 
    setup=read_and_simplify('pyLIMA_setup_2.py'), 
    stmt='chi2_telescope(your_event, model_1, parameters_list)'))

n_processes = 10 # 20 is default value.

# Main part is below.
runner = perf.Runner(processes=n_processes)
for kwargs in kwargses:
    runner.timeit(**kwargs)
