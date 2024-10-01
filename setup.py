from setuptools import setup, find_packages

setup(
    name="pdfcomparator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Pillow>=8.3.2",
        "PyMuPDF>=1.19.6",
        "numpy>=1.21.2",
        "opencv-python>=4.5.3.56",
    ],
    entry_points={
        "console_scripts": [
            "pdfcomparator=src.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for comparing PDF files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LeonardoSDJ",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)