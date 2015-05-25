from setuptools import setup

import plottags


with open("LICENSE") as fd:
    LICENSE = fd.read()

with open("README.rst") as fd:
    README = fd.read()

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
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],
)

