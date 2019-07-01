import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="odata1cw",
    version="0.0.4",
    author="Ilia Belov",
    author_email="belov.penrose@gmail.com",
    description="1C-Odata wrapper",
    long_description="1C (v8.1c.ru) OData wrapper.",
    long_description_content_type="text/markdown",
    url="https://github.com/belov38/1c-odata",
    packages=setuptools.find_packages(),
    install_requires=[
          'requests',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)