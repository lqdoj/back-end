from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from users.views import UserView
from . import views

router = routers.DefaultRouter()
router.register('', UserView, 'users')
urlpatterns = [
    path('user_login/', obtain_auth_token),
    path('user_logout/', views.logout_handle),
]
urlpatterns += router.urls

