try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

config = {
    'description':'Data Science Evaluation Tools and Utilities',
    'author': 'ross palmer',
    'license':'MIT',
    'version': '0.3.0',
    'install_requires': ['pandas','numpy'],
    'packages': find_packages(),
    'scripts': [],
    'name':'dtools'
}

setup(**config)
