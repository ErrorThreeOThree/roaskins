from distutils.core import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    long_description=long_description,
    long_description_content_type='text/markdown',
    name = 'roaskins',
    packages = ['roaskins'],
    version = '1.01',
    license = 'MIT',
    description = 'Rivals of Aether skin and color code library',
    author = 'Julian Hartmer',
    author_email = 'j.hartmer@googlemail.com',
    url = 'https://github.com/ErrorThreeOThree/roaskins',
    keywords = ['roa', 'Rivals', 'of', 'Aether', 'skin'],
    package_data={'': ['data/*/*', 'README.md']},
    include_package_data=True,
    install_requires = [
        'opencv-python',
        'numpy'
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable  ',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],

)