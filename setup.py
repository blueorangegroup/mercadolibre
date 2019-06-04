from setuptools import setup, find_packages
import sys

install_requires = [
#    'requests'
]


setup(
    name='mercadolibre',
    version='1.0.0',
    description='Mercadolibre',
    long_description='Mercadolibre',
    author='BLUEORANGE GROUP SRL',
    author_email='daniel@blueorange.com.ar',
    license='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='mercadolibre',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=install_requires,
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
)
