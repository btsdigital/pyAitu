import pathlib
import re
import sys
from setuptools import setup, find_packages

try:
    from pip.req import parse_requirements
except ImportError:
    from pip._internal.req import parse_requirements

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


def get_requirements(filename=None):
    if filename is None:
        filename = 'requirements.txt'

    file = WORK_DIR / filename

    install_reqs = parse_requirements(str(file), session='hack')
    return [str(ir.req) for ir in install_reqs]


setup(
    name="pyAitu",
    version="0.0.1",
    author="Yerassyl Zeinolla",
    author_email="yerassyl.zeinolla@btsdigital.kz",
    description="Asynchronous Python framework for Aitu Bot API",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/btsdigital/pyAitu",
    packages=find_packages(exclude=('tests', 'tests.*', 'examples.*', 'docs')),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires='>=3.7',
    install_requires=get_requirements(),
    package_data={'': ['requirements.txt']},
    include_package_data=False,
    license='Apache 2.0'
)
