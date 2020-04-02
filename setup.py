import pathlib
import re
import sys
from setuptools import setup, find_packages

WORK_DIR = pathlib.Path(__file__).parent

MINIMAL_PY_VERSION = (3, 7)
if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError('pyAitu works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))


def get_description():
    with open('README.rst', 'r', encoding='utf-8') as f:
        return f.read()


def get_version():
    txt = (WORK_DIR / 'pyAitu' / '__init__.py').read_text('utf_8')
    try:
        return re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


REQUIRED_PACKAGES = [
    'aiohttp>=3.5.4, <4.0.0',
    'certifi>=2018.8.24'
]


setup(
    name="pyAitu",
    version="0.0.6",
    author="Yerassyl Zeinolla",
    author_email="yerassyl.zeinolla@btsdigital.kz",
    description="Asynchronous Python framework for Aitu Bot API",
    long_description=get_description(),
    url="https://github.com/btsdigital/pyAitu",
    packages=find_packages(exclude=('tests', 'tests.*', 'examples.*', 'docs')),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires='>=3.7',
    install_requires=REQUIRED_PACKAGES,
    package_data={'': ['requirements.txt']},
    include_package_data=False,
    license='Apache 2.0'
)
