import os
import setuptools

from filename_sanitizer import __version__


name = 'filename-sanitizer'
description = 'Simple filename sanitization utility'
version = __version__
dependencies = ['Unidecode>=1.3.2']
entry_points = {
    'console_scripts': ['filename-sanitizer = filename_sanitizer.__main__:main']
}

setuptools.setup(
    name=name,
    version=version,
    description=description,
    author='',
    author_email='',
    license='',
    url='',
    packages=setuptools.find_packages(),
    package_data={},
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=dependencies,
    entry_points=entry_points,
    zip_safe=False
)
