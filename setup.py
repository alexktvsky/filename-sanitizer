import os
import setuptools


name = 'filename-sanitizer'
description = 'Simple filename sanitization utility'
version = '0.2.2'
dependencies = [
    'transliterate~=1.10.2',
]
extras = {}

packages = [
    package
    for package in setuptools.PEP420PackageFinder.find()
]

entry_points = {
    'console_scripts': [
        'filename-sanitizer = filename_sanitizer.main:main'
    ],
}

setuptools.setup(
    name=name,
    version=version,
    description=description,
    author='',
    author_email='',
    license='',
    url='',
    platforms='Posix; MacOS X; Windows',
    packages=packages,
    install_requires=dependencies,
    extras_require=extras,
    python_requires='>=3.7',
    include_package_data=True,
    zip_safe=False,
    entry_points=entry_points,
)
