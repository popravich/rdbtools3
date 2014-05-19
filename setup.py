import os.path
import re
from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), 'rt') as f:
        return f.read().strip()


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'rdbtools3', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            raise RuntimeError('Cannot find version in rdbtools3/__init__.py')


classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.0',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
    'Intended Audience :: Developers',
    ]

setup(name='rdbtools3',
      version=read_version(),
      description=("Redis dump.rdb parser library and cli tool"
                   " implemented with Python 3."),
      long_description='\n\n'.join((read('README.md'), read('CHANGES.txt'))),
      classifiers=classifiers,
      platforms=["POSIX"],
      author="Alexey Popravka",
      author_email="alexey.popravka@horsedevel.com",
      url="https://github.com/popravich/rdbtools3",
      license="MIT",
      packages=find_packages(exclude=["tests"]),
      include_package_data=True,
      )
