try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys, os

config = {
    'descripton': 'Tools for processing the T3 binary format for TCSPC from PicoQuant.',
    'url': 'https://github.com/vamin/T3Tools',
    'author': 'Victor Amin',
    'author_email': 'victor.amin@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['t3tools'],
    'scripts': [],
    'name': 't3tools',
    'entry_points': {'console_scripts': ['t3tools=t3tools.__main__:main']}
}

setup(**config)