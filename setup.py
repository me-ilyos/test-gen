"""
Setup script for installing the test question checker application.

This file contains the setup configuration for packaging, dependencies,
and metadata for the application.
"""

from setuptools import setup, find_packages
from typing import List


def read_requirements() -> List[str]:
    """
    Read requirements from requirements.txt file.
    
    Returns:
        List of required packages
    """
    with open('requirements.txt') as f:
        return f.read().splitlines()


def read_readme() -> str:
    """
    Read the README.md file for long description.
    
    Returns:
        Content of README.md file
    """
    with open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name="test_questions_bot",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=read_requirements(),
    
    # Metadata
    author="Me-Ilyos",
    author_email="me.ilyos101@gmail.com",
    description="Telegram bot for checking test questions and converting formats required at the University: TIU",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    keywords="test, questions, bot, telegram, education, hemis",
    
    # Project URLs
    url="https://github.com/yourusername/test-questions-bot",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/test-questions-bot/issues",
    },
    
    # Classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
    ],
    
    # Requirements
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "test-bot=src.main:main",
        ],
    },
)