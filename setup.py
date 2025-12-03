from setuptools import setup, find_packages
from better_than_yesterday._version import version

setup(
    name="better_than_yesterday",
    version=version,
    description="BetterThanYesterday Backend Flask REST service",
    packages=find_packages(),
    include_package_data=True,
    scripts=["better_than_yesterday.py"]
)
