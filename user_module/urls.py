from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register-page'),
    path('login/', views.LoginView.as_view(), name='login-page'),
    path('loginalert/<str:alert>', views.LoginAlertView.as_view(), name='login-page-alert'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('check-number/<str:username>', views.GetSecurityCodView.as_view(), name='security-cod-page'),
    path('check-number-missed/<str:username>/<time>', views.GetSecurityCodAfterMissedCodsView.as_view(),
         name='security-cod-after-4-missed-cod-page'),
    path('forgotpassswordusername', views.GetUsernameView.as_view(), name='get-username-page'),
    path('forgotpassswordusername/<str:username>/<time>', views.ForgotPasswordAfterMissedCodsView.as_view(),
         name='forgot-password-missed-cods-page'),
    path('checknumber/<username>', views.ForgotPasswordView.as_view(), name='forgot-password-page'),
    path('chnage-password/<string>', views.ChangePassword.as_view(), name='change-password-page'),
]
