from django.urls import path
from .import views



urlpatterns = [
    path('login/',views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('',views.dashboard, name='dashboard'),
    path('password_change/',views.password_change, name='password_change'),

    
    path('password_reset_request/',views.password_reset_request,
         name='password_reset_request'),
    path('password_reset_confirm/<uidb64>/<token>/',views.password_reset_confirm,
         name='password_reset_confirm'),

    path('register/',views.user_registrasion, name='user_registrasion'),

]
