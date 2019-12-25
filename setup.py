#!/usr/bin/env python3

from setuptools import setup, find_packages

REQUIRES="requirements.txt"

with open("README.md", "r") as fh:
    long_description = fh.read()

def requires(filename="requirements.txt"):
    """Returns a list of all pip requirements
    :param filename: the Pip requirement file
    (usually 'requirements.txt')
    :return: list of modules
    :rtype: list
    """
    with open(filename, 'r+t') as pipreq:
        for line in pipreq:
            line = line.strip()
            if not line or line[0:2].strip() in ("#", "##", "-r"):
                continue
            yield line

setup(
    name="azubi-timesheet",
    version="0.9.0",
    author="Elisei Roca",
    author_email="elisei.roca@gmail.com",
    description="Keep track of your work hours. Add, delete, update records. " \
        "Export and print at the end of the month!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eliroca/azubi-timesheet",
    license="MIT",
    entry_points={
        "console_scripts": [
            "azubi-timesheet=azubi_timesheet.azubi_timesheet:main"
        ]},
    project_urls={
        "Bug Tracker": "https://github.com/eliroca/azubi-timesheet/issues",
        "Documentation": "https://github.com/eliroca/azubi-timesheet/blob/master/README.md",
        "Source Code": "https://github.com/eliroca/azubi-timesheet",
        },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        ],
    keywords="azubi timesheet python track hours",
    install_requires=list(requires(REQUIRES)),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
