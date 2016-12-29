import os
from setuptools import setup, find_packages

# Dynamically parse version number from VERSION file
direc = os.path.dirname(os.path.realpath(__file__))
version = open(direc + os.sep + 'VERSION').readline().strip()


# Dynamically parse install requirements from requirements.txt
def parse_requirements(test_requirements=False):
    packages = []

    if test_requirements:
        requirements_file = open(os.path.join(direc, 'redberry', 'tests', 'requirements.txt'))
    else:
        requirements_file = open(os.path.join(direc, 'requirements.txt'))

    for line in requirements_file:
        package = line.strip()

        if not package:
            break

        packages.append(package)

    return packages

requirements = parse_requirements(test_requirements=False)
test_requirements = parse_requirements(test_requirements=True)

setup(
    name='Redberry',
    version=version,
    description='Flask Blueprint for adding simple CMS functionality',
    long_description='Flask Blueprint for adding simple CMS functionality',
    author='Michael Cho',
    author_email='michael.cho@mail.com',
    license='Apache License 2.0',
    url='https://github.com/michaelcho/redberry',

    install_requires=requirements,
    tests_require=test_requirements,
    packages=find_packages(),

    # Includes templates and static files in MANIFEST.in
    include_package_data=True,

    # Ref https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Flask',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='flask cms blog blueprint',
)
