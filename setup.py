from setuptools import setup, find_packages

install_requires = [
    'requests', 'simplejson'
]


setup(
    name='mercadolibre',
    version='2.4.5',
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
    # Los tests no forman parte del paquete distribuido.
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=install_requires,
    extras_require={},
    package_data={'mercadolibre': ['python_sdk/lib/*',]},
    data_files=[],
    entry_points={},
)
