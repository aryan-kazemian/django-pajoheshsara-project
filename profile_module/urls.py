from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile-page'),
    path('chnage-password/', views.ChangePasswordView.as_view(), name='profile-change-password-page'),
    path('purchased-courses/', views.purchased_courses, name='purchased-courses-page'),
]
