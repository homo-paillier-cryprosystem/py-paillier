from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="py_paillier",
    version="0.0.1",
    author="Vsevolod Vlasov",
    author_email="cold.vv.ss@gmail.com",
    description="A package to convert your Jupyter Notebook",
    long_description=readme,
    url="https://github.com/homo-paillier-cryprosystem/py-paillier/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8.3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)