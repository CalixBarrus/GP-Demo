import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GP_Framework_BYU_HCMI", 
    version="0.0.8",
    author="A. Anthon/C. Barrus",
    author_email="",
    description="Contains some basic genetic algorithms that can be used for arbitrary applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CalixBarrus/GP-Demo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
