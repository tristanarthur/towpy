from setuptools import setup, find_packages

setup(
    name="towpy",
    version="0.1.4",
    url="https://github.com/treestein/TOW.PY",
    author="Tristan Arthur",
    author_email="tristanarthur2000@gmail.com",
    description="Text Only Window",
    packages=find_packages(exclude=["tests"]),
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    zip_safe=False,
)
