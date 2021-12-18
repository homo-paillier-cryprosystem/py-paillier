from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="py_paillier",
    version="0.0.7",
    author="Vsevolod Vlasov",
    author_email="cold.vv.ss@gmail.com",
    description="Paillier cryptosystem",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/homo-paillier-cryprosystem/py-paillier/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
