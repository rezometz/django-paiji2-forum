# Copyright (C) 2015 Louis-Guillaume DUBOIS
#
# This file is part of Paiji-forum
#
# Paiji-forum is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# Paiji-forum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from setuptools import setup
from django.core import management

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

currentdir = os.getcwd()
os.chdir(os.path.join(currentdir, 'forum'))
management.call_command('compilemessages', stdout=sys.stdout)
os.chdir(currentdir)

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
    license='AGPLv3',
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
