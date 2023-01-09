from mypyc.build import mypycify
from setuptools import setup

setup(
    packages=["myhy"],
    ext_modules=mypycify(["--config-file=pyproject.toml", "myhy"]),
)
