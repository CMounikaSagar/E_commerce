from django.urls import path
from .views import *

urlpatterns = [
    path('register/',register,name='register'),
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('accounts/activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('dashboard/',dashboard,name='dashboard'),
    path('forgot_pwd/',forgot_pwd,name='forgot_pwd'),
     path('resetpassword_validate/<uidb64>/<token>/', resetpassword_validate, name='resetpassword_validate'),
     path('resetpassword/',resetpassword,name='resetpassword'),
     path('edit_profile/',editprofile,name='edit_profile'),
]
