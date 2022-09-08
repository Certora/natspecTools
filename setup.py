import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

NAME = "CVLDoc"
VERSION = "0.1.1"

if __name__ == "__main__":
    setuptools.setup(
        name=NAME,
        version=VERSION,
        author="Certora ltd",
        author_email="support@certora.com",
        description=" Utility for reading smart contracts files, parse and export their NatSpec comments to JSON files.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/Certora/natspecTools",
        packages=setuptools.find_packages(),
        include_package_data=True,
        install_requires=[
            'natspec_parser==0.2.1'
        ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 3 - Alpha",
        ],
        python_requires='>=3.5',
    )
