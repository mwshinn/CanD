# Copyright 2018 Max Shinn <max@maxshinnpotential.com>
# 
# This file is part of Paranoid Scientist, and is available under the
# MIT license.  Please see LICENSE.txt in the root directory for more
# information.

from setuptools import setup

with open("cand/_version.py") as f:
    exec(f.read())

with open("README.md", "r") as f:
    long_desc = f.read()

setup(
    name = 'CanD',
    version = __version__,
    description = 'Create complex layouts for scientific figures in matplotlib',
    long_description = long_desc,
    long_description_content_type='text/markdown',
    author = 'Max Shinn',
    author_email = 'm.shinn@ucl.ac.uk',
    url = 'https://github.com/mwshinn/cand',
    maintainer = 'Max Shinn',
    license = 'MIT',
    python_requires='>=3.5',
    maintainer_email = 'm.shinn@ucl.ac.uk',
    packages = ['cand'],
    install_requires = ['numpy', 'scipy', 'matplotlib', 'paranoid-scientist >= 0.2.1', 'PyMuPDF >= 1.16.0', 'Pillow'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Framework :: Matplotlib',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Visualization',
    ]
)
