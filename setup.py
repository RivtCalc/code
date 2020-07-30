from distutils.core import setup

setup(
    name='rivetcalc',
    author='rhholland',
    version='0.8.2-beta.0',
    packages=['rivetcalc','rivetcalc.unum','rivetcalc.unum.units','rivetcalc.unum.units.si'],
    license='GPLv3',
    long_description=open('README.rst').read(),
    python_requires='>=3.7',
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
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
