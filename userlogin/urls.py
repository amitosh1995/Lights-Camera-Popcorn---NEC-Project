from django.urls import path
from . import views


urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('home/', views.post_sign_in, name='post_Sign_In'),
    path('registration/', views.sign_up, name='sign_up'),
    path('registration/post_sign_up/', views.post_sign_up, name='post_Sign_Up'),
    path('home/bookseats/', views.seat_booking, name='seat_selection'),
    path('home/booking_confirmation/', views.ticket_confirmation, name='confirm_ticket')
]
