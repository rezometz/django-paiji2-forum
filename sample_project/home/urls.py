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
