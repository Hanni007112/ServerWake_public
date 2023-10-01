from django.urls import path
from . import views
from django.contrib.auth.models import Group
# to automatically ad it to the requirements when running pipreqs        import fontawesomefree 
import os
import django.db.utils

def one_time_startup():
    Group.objects.get_or_create(name='normalUser')
    Group.objects.get_or_create(name='admin')

configFilePath = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'DATA/db.sqlite3'))
if os.path.isfile(configFilePath):
    try:
        if Group.objects.exists():
            one_time_startup()
    except django.db.utils.OperationalError:
        pass

urlpatterns = [
    path('', views.home, name='home'),
    path('nextShutdown/', views.nextShutdown, name='nextShutdown'),
    path('timeTillNextShutdown/', views.timeTillNextShutdown, name='timeTillNextShutdown'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name= 'logout'),
    path('register/', views.registerPage, name='register'),
    path('poweroff/', views.power_off_Page, name='powerOff'),
    path('poweron/', views.power_on_Page, name='powerOn'),
    path('createAllocation/', views.createAllocation, name='createAllocation'),
    path('changeAllocation/', views.changeAllocation, name='changeAllocation')
]
