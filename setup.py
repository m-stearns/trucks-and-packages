from pkg_resources import find_distributions
from setuptools import setup, find_packages

setup(
    name="trucksandpackages",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
    ]
)