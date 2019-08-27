from django.urls import path

from . import views
from django.contrib.auth.views import LoginView, PasswordResetView,\
    PasswordResetDoneView, PasswordResetConfirmView

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('download', views.download, name='llamas_download'),
    path('submission', views.submission, name='submission'),
    path('benchmarks', views.benchmarks, name='benchmarks'),
    path('benchmark_binary', views.benchmark_binary, name='benchmark_binary'),
    path('benchmark_multi', views.benchmark_multi, name='benchmark_multi'),
    path('benchmark_splines', views.benchmark_splines, name='benchmark_splines'),
    path('imprint', views.imprint, name='imprint'),

    path('signup', views.signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='llamas/login.html'),
         name='login'),

    path('password_reset/', PasswordResetView.as_view(
        template_name='llamas/general_form.html', extra_context={'form_name': 'Reset Password'},
        success_url='/llamas/'),
        name='password_reset'),
    # path('password_reset/done/', PasswordResetDoneView.as_view(template_name='llamas/general_form.html', extra_context={'form_name': 'Password reset done'}), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='llamas_general_form.html', extra_context={'form_name': 'Reset Password'},
        post_reset_login=True, success_url='/llamas/'), name='password_reset_confirm'),
    # path('reset/done/', views.index, name='passwort_reset_forward'),
]
