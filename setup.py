from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    This function will return list of requirements
    """
    reqirements_list : List[str] = []
    return reqirements_list

setup (
    name = "trans",
    version = '0.0.1',
    author="Vipul Munot",
    author_email="vmunot23@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements()
)