from django.urls import path
from . import views


urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('home/', views.post_sign_in, name='postSignIn'),
    path('registration/', views.sign_up , name='sign_up')
]
