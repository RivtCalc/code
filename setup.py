from distutils.core import setup

setup(
    name='RivetCalc',
    version='0.8.2-beta.0',
    packages=['rivetcalc','rivetcalc.unum','rivetcalc.unum.units','rivetcalc.unum.units.si'],
    license='GPLv3',
    long_description=open('README.rst').read(),
    install_requires=[
   'numpy',
   'sympy',
   'pandas',
   'tabulate',
   'matplotlib',
   'jupyter',
   'docutils',
   'antlr4-python3-runtime>=4.7,<4.8'
   ]
)
