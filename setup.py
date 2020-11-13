import codecs
import os
import re
from setuptools import find_packages, setup


#  https://packaging.python.org/guides/single-sourcing-package-version/
#  #single-sourcing-the-version


def read_file(filename: str) -> str:
    """Read package file as text to get name and version"""
    # intentionally *not* adding an encoding option to open
    # see here:
    # https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, "hilbertcurve", filename), "r") as f:
        return f.read()


def find_version() -> str:
    """Only define version in one place"""
    version_file = read_file("__init__.py")
    version_match = re.search(r'^__version__ = ["\']([^"\']*)["\']', version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def find_name() -> str:
    """Only define name in one place"""
    name_file = read_file("__init__.py")
    name_match = re.search(r'^__package_name__ = ["\']([^"\']*)["\']', name_file, re.M)
    if name_match:
        return name_match.group(1)
    raise RuntimeError("Unable to find name string.")


def find_long_description() -> str:
    """Return the content of the README.rst file."""
    return read_file("../README.rst")


setup(
    name=find_name(),
    version=find_version(),
    description="Construct Hilbert Curves.",
    long_description=find_long_description(),
    long_description_content_type="text/x-rst",
    url="https://github.com/galtay/hilbertcurve",
    author="Gabriel Altay",
    author_email="gabriel.altay@gmail.com",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "numpy",
    ],
    extras_require={
        "dev": ["sphinx", "sphinx_rtd_theme", "sphinx_autodoc_typehints", "pytest"]
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="fractal space-filling-curves hilbert hilbert-curve python python3 wikidata parser",
    python_requires=">=3.6",
)
