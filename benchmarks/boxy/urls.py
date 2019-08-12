from django.urls import path

from . import views
from django.contrib.auth.views import LoginView, PasswordResetView,\
    PasswordResetDoneView, PasswordResetConfirmView

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('download', views.download, name='boxy_download'),
    path('submission', views.submission, name='boxy_submission'),
    path('benchmarks', views.benchmarks, name='benchmarks'),
    path('benchmark_2d', views.benchmark_2d, name='benchmark_2d'),
    path('benchmark_3d', views.benchmark_3d, name='benchmark_3d'),
    path('benchmark_realtime', views.benchmark_realtime, name='benchmark_realtime'),
    path('imprint', views.imprint, name='imprint'),

    path('signup', views.signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='boxy/login.html'),
         name='login'),

    path('password_reset/', PasswordResetView.as_view(
        template_name='boxy/general_form.html', extra_context={'form_name': 'Reset Password'}), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='boxy/general_form.html', extra_context={'form_name': 'Password reset done'}), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='boxy_general_form.html', extra_context={'form_name': 'Reset Password'}), name='password_reset_confirm'),
    path('reset/done/', views.index, name='passwort_reset_forward'),
]
