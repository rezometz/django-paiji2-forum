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

from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
] + i18n_patterns(
    url(r'^', include('home.urls')),
    url(r'^', include('forum.urls', namespace='forum')),
    url(r'^admin/', include(admin.site.urls)),
)
