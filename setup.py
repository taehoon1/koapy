#!/usr/bin/env python

"""The setup script."""

from __future__ import annotations

from setuptools import find_packages, setup

with open("README.rst", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", encoding="utf-8") as history_file:
    history = history_file.read()

requirements = [
    "click>=7.1.2",
    "discord.py>=1.7.2",
    "exchange-calendars>=3.0.2",
    "grpcio>=1.37.1",
    "grpcio-tools>=1.37.1",
    "korean-lunar-calendar>=0.2.1",
    "numpy>=1.20.2",
    "openpyxl>=3.0.7",
    "pandas>=1.2.4",
    "protobuf>=3.16.0",
    "pyhocon>=0.3.57",
    "PySide2>=5.15.2",
    "pytz>=2021.1",
    "QtPy>=1.9.0",
    "requests>=2.25.1",
    "Rx>=3.2.0",
    "schedule>=1.1.0",
    "Send2Trash>=1.5.0",
    "SQLAlchemy>=1.4.14",
    "tabulate>=0.8.9",
    "tqdm>=4.60.0",
    "tzlocal>=2.1",
    "wrapt>=1.12.1",
    "pywin32>=300;sys_platform=='win32'",
    "pywinauto>=0.6.8;sys_platform=='win32'",
]

requirements_dev = [
    "actions-toolkit>=0.0.5",
    "black>=21.5b0",
    "bump2version>=1.0.1",
    "codecov>=2.1.11",
    "coverage>=5.5",
    "dunamai>=1.5.5",
    "flake8>=3.9.1",
    "isort>=5.8.0",
    "mypy>=0.812",
    "pip-tools>=6.1.0",
    "pre-commit>=2.12.1",
    "pylint>=2.8.2",
    "pytest>=6.2.4",
    "pytest-cov>=2.11.1",
    "pytest-xdist>=2.2.1",
]

requirements_docs = [
    "Sphinx>=3.5.4",
    "sphinx-autoapi>=1.8.1",
    "nbsphinx>=0.8.4",
    "ipython>=7.23.1",
]

requirements_dev += requirements_docs

setup(
    author="Yunseong Hwang",
    author_email="kika1492@gmail.com",
    python_requires=">=3.7.1",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Kiwoom Open Api Plus Python",  # noqa: E501
    setup_requires=[
        "setuptools-git",
    ],
    install_requires=requirements,
    extras_require={
        "dev": requirements_dev,
        "docs": requirements_docs,
        "backtarder": ["backtrader>=1.9.76", "matplotlib>=3.4.2"],
        "PyQt5": ["PyQt5>=5.15.4"],
    },
    license="MIT",
    long_description=readme + "\n\n" + history,
    name="koapy",
    packages=find_packages(include=["koapy", "koapy.*"]),
    include_package_data=True,
    test_suite="tests",
    url="https://github.com/elbakramer/koapy",
    version="0.3.5",
    zip_safe=False,
)
