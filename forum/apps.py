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
from django.apps import AppConfig

class ForumConfig(AppConfig):

    name = 'forum'
    verbose_name = 'forum'

    def ready(self):
       from forum import update_db
       update_db.update_icons_db()
