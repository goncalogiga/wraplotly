#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name='edunets',
    version='1.0',
    description='A small wrapper around plotly to have easier access to some of the functions I use most when doing data anlysis.',
    license='MIT',
    packages=['wraplotly'],
    install_requires=['numpy', 'plotly'],
    python_requires='>=3.6',
)