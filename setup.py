from setuptools import setup, find_packages
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open( 'README.md', encoding = 'utf-8' ) as f:
    long_description = f.read()

setup(

    name = 'markovdrummer',
    version = '0.1a',
    description = 'A drum beat analyzer and generator based on Markov chains',
    long_description = long_description,
    url = 'http://documentup.com/mapio/markovdrummer',

    # Author details
    author = 'Massimo Santini, and Raffaella Migliaccio',
    author_email = 'massimo.santini@unimi.it',

    # Choose your license
    license = 'GPLv3',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Education',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Multimedia :: Sound/Audio :: MIDI',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],

    keywords = 'midi analysis generation markov chain',

    packages = find_packages(),

    data_files = [ ( 'data', [ 'data/bossa.mid', 'data/quarter.mid', 'data/sixteenth.mid' ] ) ],

    entry_points={
        'console_scripts': [
            'analyze=markovdrummer.scripts.analyze:main',
            'draw=markovdrummer.scripts.draw:main',
            'generate=markovdrummer.scripts.generate:main',
            'merge=markovdrummer.scripts.merge:main',
            'preprocess=markovdrummer.scripts.preprocess:main',
            'quantize=markovdrummer.scripts.quantize:main',
            'stats=markovdrummer.scripts.stats:main',
            'test=markovdrummer.scripts.test:main'
        ],
    },
)
