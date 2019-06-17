import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="odata1c",
    version="0.0.1",
    author="Ilia Belov",
    author_email="belov.penrose@gmail.com",
    description="1C-Odata wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/belov38/1c-odata",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: unlicense :: unlicense",
        "Operating System :: OS Independent",
    ],
)