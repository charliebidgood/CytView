from setuptools import setup

setup(
    name='cytview',
    author='Charles Bidgood',
    packages=['cytview'],
    install_requires=['matplotlib>=3.6.0', 
                      'seaborn>=0.12.0',
                      'numpy>=1.23.3', 
                      'pandas>=1.5.0',
                      'scipy>=1.11.1'],
    version='1.1.1',
    license='MIT',

)
