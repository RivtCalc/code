from distutils.core import setup

setup(
    name='r-i-v-e-t',
    version='0.9dev',
    packages=['rivet','rivet.unum','rivet.unum.units','rivet.unum.units.si'],
    license='GPLv3',
    long_description=open('README.rst').read(),
)