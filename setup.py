from pathlib import Path

from setuptools import setup, find_packages

README = (Path(__file__).parent / "README.md").read_text()

setup(
    name='arithmetic-dice-roller',
    version='0.2.1',
    description="A handy dice roller with extended notation and arithmetic expressions management.",
    long_description=README,
    long_description_content_type="text/markdown",
    author='Massimo Pavoni',
    author_email='maspavoni@gmail.com',
    url='https://github.com/massimopavoni/arithmetic-dice-roller',
    license_files='LICENSE',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Operating System :: OS Independent"
    ],
    platforms=['OS Independent'],
    packages=find_packages(),
    include_package_data=True,
    python_requires='==3.10.1',
    install_requires=['sympy==1.9'],
    entry_points={
        'console_scripts': [
            'arithmetic-dice-roller=arithmetic_dice_roller.__main__:main'
        ]
    }
)
