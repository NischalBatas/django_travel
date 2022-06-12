from django.urls import path
from . import views
urlpatterns=[
    path('login',views.logins,name="logins"),
    path('logout',views.logouts,name="logout"),
    path('signup',views.signup,name="signup"),
    path('list',views.list,name="list"),
    path('contact',views.contact,name='contact')

]