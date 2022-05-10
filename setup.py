from pathlib import Path

from setuptools import setup, find_packages

from src import call_throttle


setup(
    name='call-throttle',
    version=call_throttle.__version__,
    description='A decorator used to throttle calls of regular functions and asyncio coroutines.',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    author='Konstantin Tolstikhin',
    author_email='k.tolstikhin@gmail.com',
    url='https://github.com/ktolstikhin/call-throttle.git',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.7',
    install_requires=[],
    keywords=[
        'decorator',
        'throttle',
        'ratelimit'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
    ],
    zip_safe=False,
)
