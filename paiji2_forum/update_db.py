# Copyright (C) 2015 Louis-Guillaume DUBOIS
#
# This file is part of paiji2-forum
#
# paiji2-forum is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# paiji2-forum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from . import __path__
from models import MessageIcon
from django.core.exceptions import *
from glob import glob


def update_icons_db():
    path = __path__[0]
    files = glob(path + '/static/forum/icons/*.jpg')\
        + glob(path + '/static/forum/icons/*.gif')\
        + glob(path + '/static/forum/icons/*.png')
    for j in files:
        i = j.split('/').pop()
        try:
            MessageIcon.objects.get(filename=i)
        except ObjectDoesNotExist:
            MessageIcon(name=i, filename=i).save()
            print "file {} added".format(i)
        except MultipleObjectsReturned:
            print "{} is not unique".format(i)
        except:
            pass
