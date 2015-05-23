from setuptools import setup

import plottags


#with open("LICENSE") as fd:
#    LICENSE = fd.read()

LICENSE = ''
README = ''

setup(
    name='plottags',
    version=plottags.__version__,
    description='A package for plotting the tag history of repositories',
    license=LICENSE,
    long_description=README,
    author=plottags.__author__,
    author_email=plottags.__email__,
    url='https://github.com/logston/plottags',
    packages=['plottags'],
    include_package_data=True,
    test_suite='tests',
    keywords=['repository', 'git', 'hg', 'mercurial', 'plot', 'tag', 'tags'],
    entry_points={
        'console_scripts': ['plottags=plottags.controller:main'],
    },
    install_requires=[
        'matplotlib>=1.4.2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)

