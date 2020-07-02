from distutils.core import setup

setup(
    name='rivetcalc',
    version='0.9dev',
    packages=['rivet','rivet.unum','rivet.unum.units','rivet.unum.units.si'],
    license='GPLv3',
    long_description=open('README.rst').read(),
    install_requires=[
   'numpy',
   'sympy',
   'pandas',
   'tabulate',
   'matplotlib'
   ]
)
