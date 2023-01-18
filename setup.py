from mypyc.build import mypycify
from setuptools import setup

setup(ext_modules=mypycify(["--config-file=pyproject.toml", "myhy"]))
