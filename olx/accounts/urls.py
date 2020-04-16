from django.urls import path
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from . import views
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    path('login/',auth_view.LoginView.as_view(), name = 'login'),
    path('password_change/',auth_view.PasswordChangeView.as_view(), name = 'password_change'),
    path('password_change/done',auth_view.PasswordChangeDoneView.as_view(), name = 'password_change_done'),
    path('password_reset/',auth_view.PasswordResetView.as_view(), name = 'password_reset'),
    path('password_reset/done/',auth_view.PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('logout',views.logout,name = 'logout'),
    path('signup',views.signup_view, name = 'signup'),
    path('activate/<uidb64>/<token>/',views.activateAccount,name='activate')

]