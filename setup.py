from setuptools import setup, find_packages
import os.path
import re

# reading package's version (same way sqlalchemy does)
with open(
    os.path.join(os.path.dirname(__file__), 'english_classroom', '__init__.py')
) as v_file:
    package_version = \
        re.compile('.*__version__ = \'(.*?)\'', re.S)\
        .match(v_file.read())\
        .group(1)


dependencies = [
    'python-telegram-bot==11.1.0',
]


setup(
    name='bankofficer',
    version=package_version,
    author='Mohamad Khajezade',
    author_email='khajezade.mohamad@gmail.com',
    description='A balebot to simulate an English classroom',
    install_requires=dependencies,
    packages=find_packages(),
)
