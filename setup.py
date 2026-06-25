#!/usr/bin/env python3
# Copyright (c) 2025 Conxian-Labs
# This software is released under the MIT License.
# See the LICENSE file in the project root for full license information.

"""
ConxiusOrbit Setup Configuration
Professional GUI deployment tool for Stacks blockchain smart contracts
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = (
    readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""
)

setup(
    name="conxius_orbit",
    version="1.2.9",
    description="CLI-first deployment and operations toolkit for Stacks / Clarity smart contracts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Conxian-Labs",
    author_email="dev@anyachainlabs.com",
    url="https://github.com/Conxian/conxius_orbit",
    project_urls={
        "Bug Tracker": "https://github.com/Conxian/conxius_orbit/issues",
        "Documentation": "https://conxian.github.io/conxius_orbit/",
        "Source Code": "https://github.com/Conxian/conxius_orbit",
        "Discussions": "https://github.com/Conxian/conxius_orbit/discussions",
    },
    packages=find_packages(exclude=["tests*", "docs*"]),
    py_modules=["conxius_orbit"],
    entry_points={
        "console_scripts": [
            "conxius_orbit=conxius_orbit:main",
        ],
    },
    python_requires=">=3.8",
    install_requires=[
        # Python standard library modules (no additional dependencies needed)
        # tkinter is included with Python
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio",
            "black>=23.0.0",
            "pylint>=2.17.0",
            "mypy>=1.0.0",
            "types-requests",
            "types-toml",
            "safety>=3.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-mock>=3.10.0",
            "pytest-asyncio",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Environment :: X11 Applications",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Topic :: Software Development",
        "Topic :: Utilities",
        "Topic :: System :: Systems Administration",
        "Framework :: AsyncIO",
    ],
    keywords=[
        "stacks",
        "blockchain",
        "smart-contracts",
        "deployment",
        "clarity",
        "gui",
        "devtools",
        "web3",
        "clarinet",
        "defi",
        "cryptocurrency",
        "bitcoin",
    ],
    license="MIT",
    platforms=["any"],
    include_package_data=True,
    package_data={
        "conxius_orbit": [
            "*.md",
            "LICENSE",
            "requirements.txt",
        ],
    },
    zip_safe=False,
)
