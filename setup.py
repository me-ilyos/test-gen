"""
Setup script for installing the test question converter bot.
"""

from setuptools import setup, find_packages

setup(
    name="test_questions_bot",
    version="1.0.0",
    packages=find_packages(),
    # Dependencies
    install_requires=[
        "python-telegram-bot>=13.0",
        "python-docx>=0.8.10",
        "python-dotenv>=0.19.0",
    ],
    # Metadata
    author="Me-Ilyos",
    author_email="me.ilyos101@gmail.com",
    description="Telegram bot for converting test questions between different formats",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    # Project URLs
    url="https://github.com/yourusername/test-questions-bot",
    # Classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
    ],
    # Requirements
    python_requires=">=3.7",
    # Entry points
    entry_points={
        "console_scripts": [
            "test-questions-bot=src.main:main",
        ],
    },
)
