import requests

from django import forms
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

from django.shortcuts import redirect
from django.shortcuts import render, render_to_response
from django.template import loader

from captcha.fields import ReCaptchaField


def bad_request(request, exception, template_name="boxy/404.html"):
    response = render_to_response("boxy/404.html")
    response.status_code = 404
    return response


def index(request):
    index_template = loader.get_template('boxy/index.html')
    context = dict()
    return HttpResponse(index_template.render(context, request))


@login_required(login_url='../boxy/login')
def download(request):
    index_template = loader.get_template('boxy/download_links.html')
    context = dict()
    return HttpResponse(index_template.render(context, request))


class SubmissionForm(ModelForm):
    model_file = forms.FileField()
    class Meta:
        model = Submission
        fields = ['user', 'speed', 'env', 'external_used',
                  'paper', 'repo', 'comments_private', 'comments_public']


# TODO @login_required(login_url='../llamas/login')
def submission(request):

    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission_instance = form.save(commit=False)
            submission_instance.user = 'karsten'  # TODO
            # TODO change upload path
            submission_instance.save()
            return HttpResponseRedirect('/llamas/')
        print('Form not valid')
    else:
        form = SubmissionForm(initial={'user': 'karsten'})  # TODO

    return render(request, 'llamas/submission.html',
                  {'form': form, 'error': 'Not working yet! Tomorrow!'})


def contact(request):
    index_template = loader.get_template('boxy/contact.html')
    context = dict()
    return HttpResponse(index_template.render(context, request))


def benchmarks(request):
    # TODO Add links to other benchmarks here
    index_template = loader.get_template('boxy/benchmarks.html')
    context = dict()
    return HttpResponse(index_template.render(context, request))


def benchmark_2d(request):
    index_template = loader.get_template('boxy/benchmark_base.html')
    context = dict()
    # TODO results
    context['results'] = [{'Name': 'Dummy model', 'AP': 14, 'MAP': 17},
                          {'Name': 'Dummy model', 'AP': 14, 'MAP': 17}]
    context['keys'] = list(context['results'][0].keys())
    context['benchmark_name'] = 'Traditional Vehicle Detection'
    context['benchmark_short'] = 'Detecting vehicles with axes-aligned bounding boxes'
    return HttpResponse(index_template.render(context, request))


def benchmark_3d(request):
    index_template = loader.get_template('boxy/benchmark_base.html')
    context = dict()
    # TODO results
    context['results'] = [{'Name': 'Dummy model', 'AP': 14, 'MAP': 17},
                          {'Name': 'Dummy model', 'AP': 14, 'MAP': 17}]
    context['keys'] = list(context['results'][0].keys())
    context['benchmark_name'] = '3D-like boxes / Polygons'
    context['benchmark_short'] = 'Higher accuracy detections by detecting visible sides'
    return HttpResponse(index_template.render(context, request))


def benchmark_realtime(request):
    index_template = loader.get_template('boxy/benchmark_base.html')
    context = dict()
    # TODO results
    context['results'] = [{'Name': 'Dummy model', 'AP': 14, 'MAP': 17},
                          {'Name': 'Dummy model', 'AP': 14, 'MAP': 17}]
    context['keys'] = list(context['results'][0].keys())
    context['benchmark_name'] = 'Realtime Vehicle Detection'
    context['benchmark_short'] = 'Everything under 50 ms'
    return HttpResponse(index_template.render(context, request))


def imprint(request):
    index_template = loader.get_template('boxy/imprint.html')
    context = {'project_name': 'The Boxy Dataset', 'project_url': 'https://www.boxy-dataset.com'}
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
                return redirect('boxy_download')
        else:
            error = '--> You need to accept the license <--'
    else:
        form = SignUpForm()

    return render(request, 'boxy/signup.html',
                  {'form': form, 'error': error, 'form_name': 'Register'})
