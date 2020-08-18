import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="test-folder-bmmauri",
    version="0.0.7",
    author="Maurizio Bussi",
    author_email="maurizio.bussi.mb@gmail.com",
    description="Test Automation framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bmmauri/test-folder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
