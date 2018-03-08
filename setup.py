import os
from setuptools import setup, find_packages


setup(
    name='autodot',
    version='0.1.0',
    author='ecleya',
    author_email='ecleya' '@' 'gmail.com',
    maintainer='ecleya',
    maintainer_email='ecleya' '@' 'gmail.com',
    url='https://github.com/ecleya/autodot',
    license='Proprietary',
    platforms='POSIX',
    description='dotfiles generator for macOS (Python)',
    packages=find_packages(exclude=['tests']),
    package_data={},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pyaml'
    ],
    py_modules=['autodot'],
    entry_points={
        'console_scripts': [
            'autodot=autodot:main',
        ]
    }
)
