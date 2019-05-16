import requests

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader

from captcha.fields import ReCaptchaField


def index(request):
    index_template = loader.get_template('llamas/index.html')
    context = dict()
    return HttpResponse(index_template.render(context, request))


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def _grecaptcha_verify(recaptcha_response, request):
    """ Actually checking if human """
    if not recaptcha_response:
        return False
    # site_key = '6LfCS20UAAAAAGfOFb3llx-MXWsRWdVRxMAEmEPs'
    secret_recaptcha_key = '6LfCS20UAAAAAD3OtbLB9wC65ug3BFdYMO7iwVV8'
    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {
        'secret': secret_recaptcha_key,
        'response': recaptcha_response,
        'remoteip': _get_client_ip(request)
    }
    verify_rs = requests.get(url, params=params, verify=True)
    verify_rs = verify_rs.json()
    return verify_rs.get("success", False)


@login_required(login_url='../llamas/login')
def download(request):
    index_template = loader.get_template('llamas/download_links.html')
    context = dict()
    return HttpResponse(index_template.render(context, request))


def contact(request):
    index_template = loader.get_template('llamas/contact.html')
    context = dict()
    return HttpResponse(index_template.render(context, request))


def benchmarks(request):
    # TODO Add links to other benchmarks here
    index_template = loader.get_template('llamas/benchmarks.html')
    context = dict()
    return HttpResponse(index_template.render(context, request))


def benchmark_binary(request):
    index_template = loader.get_template('llamas/benchmark_base.html')
    context = dict()
    # TODO results
    context['results'] = [{'Name': 'Dummy Model', 'AP': 14, 'MAP': 17},
                          {'Name': 'Dummy Model', 'AP': 14, 'MAP': 17}]
    context['keys'] = list(context['results'][0].keys())
    context['benchmark_name'] = 'Binary Lane Marker Segmentation'
    context['benchmark_short'] = 'Decide whether a pixel belongs to a lane marker or not'
    return HttpResponse(index_template.render(context, request))


def benchmark_multi(request):
    index_template = loader.get_template('llamas/benchmark_base.html')
    context = dict()
    # TODO results
    context['results'] = [{'Name': 'Dummy Model', 'AP': 14, 'MAP': 17},
                          {'Name': 'Dummy Model', 'AP': 14, 'MAP': 17}]
    context['keys'] = list(context['results'][0].keys())
    context['benchmark_name'] = 'Multi-class Lane Marker Segmentation'
    context['benchmark_short'] = 'Decide whether a pixel belongs to a marker and assign it to a lane'
    return HttpResponse(index_template.render(context, request))


def benchmark_splines(request):
    index_template = loader.get_template('llamas/benchmark_base.html')
    context = dict()
    # TODO results
    context['results'] = [{'Name': 'Dummy Model', 'AP': 14, 'MAP': 17},
                          {'Name': 'Dummy Model', 'AP': 14, 'MAP': 17}]
    context['keys'] = list(context['results'][0].keys())
    context['benchmark_name'] = 'Lane Approximations'
    context['benchmark_short'] = 'Because curves can be easier to handle than a few thousand pixels'
    return HttpResponse(index_template.render(context, request))


def imprint(request):
    index_template = loader.get_template('llamas/imprint.html')
    context = {'project_name': 'The Unsupervised Lllamas dataset',
               'project_url': 'https://www.unsupervised-lllamas.com'}
    return HttpResponse(index_template.render(context, request))


class SignUpForm(UserCreationForm):
    recaptcha = ReCaptchaField(label="I'm a human")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')


def signup_view(request):
    error = ''
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if 'license' in request.POST and request.POST['license'] == 'on':
          if form.is_valid():
              if User.objects.filter(email=form.instance.email).exists():
                  error = 'Email is already registered'

              if not error:
                user = form.save()
                login(request, user)
                return redirect('llamas_download')
        else:
            error = '--> You need to accept the license <--'
    else:
        form = SignUpForm()

    return render(request, 'llamas/signup.html',
                  {'form': form, 'error': error, 'form_name': 'Register'})
