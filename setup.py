import os
import sys
import subprocess
import warnings
from setuptools import setup
from setuptools.command.install import install


dir_ = os.path.join('lib', 'python' + sys.version[:3], 'site-packages', 
                    'MulensModel')

source_VBBL = os.path.join('source', 'VBBL')
source_AC = os.path.join('source', 'AdaptiveContouring')
source_MM = os.path.join('source', 'MulensModel')
source_MMmo = os.path.join(source_MM, 'mulensobjects')

wrapper_VBBL = os.path.join(source_VBBL, 'VBBinaryLensingLibrary_wrapper.so')
wrapper_AC = os.path.join(source_AC, 'AdaptiveContouring_wrapper.so')

data_files = [ (os.path.join(dir_, 'data'), [os.path.join('data', 'interpolation_table_b0b1_v1.dat')]) ]

version = "unknown"
with open(os.path.join('source', 'MulensModel', 'version.py')) as in_put:
    for line_ in in_put.readlines():
        if line_.startswith('__version__'):
            version = line_.split()[2][1:-1]


class CustomInstall(install):
    """
    Custom install procedure that runs makefiles.
    """
    def run(self):
        print("Begin running makefiles...")
        subprocess.call(["make", "-C", source_VBBL])
        subprocess.call(["make", "-C", source_AC])
        print("Finish running makefiles...")
        if os.path.isfile(wrapper_VBBL):
            data_files.append( 
                            (os.path.join(dir_, source_VBBL), [wrapper_VBBL]) )
        else:
            msg = "Makefile failed to produce: {:}\n!!!"
            warnings.warn(msg.format(wrapper_VBBL))

        if os.path.isfile(wrapper_AC):
            data_files.append( (os.path.join(dir_, source_AC), [wrapper_AC]) )
        else:
            msg = "Makefile failed to produce: {:}\n!!!"
            warnings.warn(msg.format(wrapper_AC))

        install.run(self)

setup(
    name='MulensModel',
    version=version,
    url='git@github.com:rpoleski/MulensModel.git',
    cmdclass={'install': CustomInstall},
    author='Radek Poleski',
    author_email='poleski.1@osu.edu',
    description='packge for modeling gravitational microlensing events',
    packages=['MulensModel', 'MulensModel.mulensobjects'],
    package_dir={
        'MulensModel': source_MM,
        'MulensModel.mulensobjects': source_MMmo},
    data_files=data_files,
    install_requires=['numpy', 'matplotlib', 'scipy', 'astropy>=1.2.0']
)

