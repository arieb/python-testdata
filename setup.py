import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "python-testdata",
    version = "1.0",
    author = "Arie Bro",
    description = "A small package that helps generate content to fill databases for tests.",
    license = "MIT",
    package_data = {
        '': ['.md']
    },
    install_requires = [
        'fake-factory == 0.2'
    ],
    keywords = "mongodb factory testing test unittest mongo data testdata database json",
    packages = ['testdata', 'testdata.extra', 'testdata.factories'],
    long_description=read('README.md'),
    classifiers=[
        "Topic :: Testdata",
        "License :: MIT License",
    ],
)
