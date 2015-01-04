from setuptools import setup

setup(
    name='cpsk',
    
    description='an unofficial api for grabbing data from cp.sk',
    author='Adrian Matejov',
    author_email='a.matejov@centrum.sk',
    version='0.0.9',
   
    url='https://github.com/Adman/python-cpsk-api',

    install_requires=['requests', 'lxml'],
    include_package_data=True,
    packages=['cpsk'],

    license="The MIT License (MIT)"
)
