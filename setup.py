from distutils.core import setup

setup(
    name = 'roaskins',
    packages = ['roaskins'],
    version = '0.31',
    license = 'MIT',
    description = 'Rivals of Aether skin and color code library',
    author = 'Julian Hartmer',
    author_email = 'j.hartmer@googlemail.com',
    url = 'https://github.com/ErrorThreeOThree/roaskins',
    keywords = ['roa', 'Rivals', 'of', 'Aether', 'skin'],
    install_requires = [
        'opencv-python',
        'numpy'
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],

)