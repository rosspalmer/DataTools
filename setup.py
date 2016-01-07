try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

config = {
    'description':'Data Mining and Analysis Tools',
    'author': 'ross palmer',
    'license':'MIT',
    'version': '0.2.3',
    'install_requires': ['pandas','numpy'],
    'packages': find_packages(),
    'scripts': [],
    'name':'dtools'
}

setup(**config)
