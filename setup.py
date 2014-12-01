from setuptools import setup

setup(
    name='cpsk',
    
    description='an unofficial api for grabbing data from cp.sk',
    author='Adrian Matejov',
    author_email='a.matejov@centrum.sk',
    version='0.0.3',
   
    url='https://github.com/Adman/python-cpsk-api',
    
    include_package_data=True,
    packages=['cpsk'],

    license=open('./LICENSE').read()
)
