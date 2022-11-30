from setuptools import setup


with open('README.md') as f:
    long_description = f.read()

setup(
    name='cpsk',
    description='an unofficial api for grabbing data from cp.sk',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Adrian Matejov',
    author_email='a.matejov@centrum.sk',
    version='0.2.1',
    url='https://github.com/Adman/python-cpsk-api',
    install_requires=['requests', 'lxml'],
    include_package_data=True,
    packages=['cpsk'],
    license="The MIT License (MIT)",
    keywords=['travel', 'train', 'bus']
)
