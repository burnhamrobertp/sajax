"""
sajax
-------------

Flask / jQuery AJAX library, structured similarly to old xajax library
"""
from setuptools import setup

setup(
    name='sajax',
    version='0.11',
    url='https://github.com/harkenn/sajax',
    license='BSD',
    author='Robert Burnham',
    author_email='burnhamrobertp@gmail.com',
    description="Python / Flask / jQuery AJAX library",
    long_description=__doc__,
    packages=['sajax'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.9'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)