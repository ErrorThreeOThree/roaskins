import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'roaskins',
    setup_requires=['wheel'],
    version = '0.1',
    scripts = ['roaskins'],
    author = "Julian Hartmer",
    author_email = "j.hartmer@googlemail.com",
    description = "A Rivals of Aether skin generation library",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "GIT",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating Systems: :: OS Independent"
    ]
)