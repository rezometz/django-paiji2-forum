import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-paiji-forum',
    version='0.1',
    packages=['forum'],
    include_package_data=True,
    description='A simple forum app',
    long_description=README,
    url='https://github.com/rezometz/django-paiji-forum',
    author='Louis-Guillaume DUBOIS',
    author_email='contact@lgdubois.fr',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
