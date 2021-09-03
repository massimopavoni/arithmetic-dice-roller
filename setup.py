from pathlib import Path

from setuptools import setup

README = (Path(__file__).parent / "README.md").read_text()

setup(
    name='arithmetic-dice-roller',
    version='a0.0.1',
    description='A handy dice roller with extended notation and arithmetic expressions management.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/Damax00/arithmetic-dice-roller',
    author='Massimo Pavoni',
    author_email='maspavoni@gmail.com',
    license='GNU General Public License v3.0',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python"
    ],
    packages=['arithmetic-dice-roller'],
    include_package_data=True,
    install_requires=[""],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)
