from setuptools import setup

setup(
    name='cytview',
    author='Charles Bidgood',
    packages=['cytview'],
    install_requires=['matplotlib==3.3.4', 
                      'seaborn==0.11.1',
                      'numpy==1.21.6', 
                      'pandas==1.3.0',
                      'scipy==1.7.3'],
    version='1.0.0',
    license='MIT',

)
