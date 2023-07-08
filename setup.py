from setuptools import setup, find_packages

description = "This module can be used to help in authentication and managing login/logout or sessions on the web"
with open("readme.md", "r") as file:
    long_description = file.read()

setup(
    name="login_handler",
    version="0.0.1",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Pankaj",
    author_email="pankaj.vishw.dev@gmail.com",
    url="https://github.com/PankajVishw50/login_handler.git",
    packages=find_packages("app"),
    package_dir={"": "app"},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 ",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[
        "cipher_kit==0.0.4"
    ],
    extra_requires={
        "dev": [
            "pytest>=7.0.0",
            "flask>=2.3.0"
        ]
    }
)
