from django.urls import path
from .views import Registration,UserLogin,UserLogout,AdminLogin

urlpatterns = [

    path('registration/',Registration.as_view()),
    path('userlogin/',UserLogin.as_view()),
    path('adminlogin/',AdminLogin.as_view()),
    path('logout/',UserLogout.as_view()),

]
