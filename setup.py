from setuptools import find_packages, setup

setup(
    name="mofeapi",
    version="0.1.3",
    author="Ryohei Kobayashi",
    author_email="kobaryo222912@gmail.com",
    description="Unofficial Python wrapper for MOFE API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ryohei222/mofeapi-python",
    packages=find_packages(),
    package_data={"mofeapi": ["py.typed"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
