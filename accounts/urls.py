from django.urls import path
#from accounts.views import *
from accounts.views import * 


app_name = 'accounts'

urlpatterns = [
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogOut.as_view(),name='logout'),
    #path('singup/',singup_view,name='singup'),
    path('register/',RegisterView.as_view(),name='singup'),   
]