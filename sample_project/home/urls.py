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

from django.conf.urls import url
from django.contrib.auth.views import login, logout, password_change

urlpatterns = [
    url(
        r'^login/',
        login,
        dict(
            template_name='home/login.html',
        ),
        name='login',
    ),
    url(
        r'^logout/',
        logout,
        dict(
            next_page='/',
        ),
        name='logout'
    ),
    url(
        r'^password_change/',
        password_change,
        dict(
            post_change_redirect='/',
            template_name='home/password_change.html',
        ),
        name='password_change',
    ),
]
