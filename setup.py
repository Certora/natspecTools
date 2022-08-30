import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

NAME = "certora-natspec"
VERSION = "0.1.0"

if __name__ == "__main__":
    setuptools.setup(
        name=NAME,
        version=VERSION,
        author="Certora",
        author_email="support@certora.com",
        description=" Utility for reading smart contracts files, parse and export their NatSpec comments to JSON files.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/Certora/natspecTools",
        packages=setuptools.find_packages(),
        include_package_data=True,
        install_requires=[],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 3 - Alpha",
        ],
        # entry_points={
        #     "console_scripts": [
        #         "natspec = certora_cli.certoraRun:entry_point"
        #     ]
        # },
        python_requires='>=3.5',
    )
