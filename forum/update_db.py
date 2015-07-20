from forum import __path__
from forum.models import MessageIcon
from django.core.exceptions import *
from glob import glob

def update_icons_db():
    path = __path__[0]
    for j in glob(path + '/static/forum/icons/*.jpg')\
        + glob(path + '/static/forum/icons/*.gif')\
        + glob(path + '/static/forum/icons/*.png'):
        i = j.split('/').pop() 
        try:
            MessageIcon.objects.get(filename=i)
        except ObjectDoesNotExist:
            MessageIcon(name=i, filename=i).save()
            print "fichier {} ajoute".format(i)
        except MultipleObjectsReturned:
            print "{} n'est pas unique".format(i)
        except:
            pass
