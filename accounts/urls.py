"""
/accounts URL Configuration
"""
from django.conf.urls import include
from django.urls import path
from accounts.views import logout, login, registration, user_profile, update_profile
from accounts import url_reset

urlpatterns = [
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('register/', registration, name='registration'),
    path('profile/', user_profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('password-reset/', include(url_reset))
]

