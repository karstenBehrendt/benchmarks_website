import datetime
import os
import requests

from django import forms
from django.forms import ModelForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

from django.shortcuts import redirect
from django.shortcuts import render, render_to_response
from django.template import loader

from captcha.fields import CaptchaField

from boxy.models import Submission

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
    europe_server = 'http://5.9.71.146'
    current_simlink = 'dqrtq7zmfsr4q59crcya'
    context = {'europe_server': europe_server, 'current_simlink': current_simlink}
    index_template = loader.get_template('boxy/download_links.html')
    return HttpResponse(index_template.render(context, request))


class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['user', 'results_url', 'model_name', 'speed', 'env', 'external_used',
                  'paper', 'email', 'repo', 'comments_private', 'comments_public']


@login_required(login_url='../boxy/login')
def submission(request):
    # NOTE Pretty much the same in boxy. Should be combined
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            content_str = "\n".join([f"{field}: {form.cleaned_data[field]}" for field in SubmissionForm.fields])

            email_from = "boxy." + "llamas" + "@" + "gmail.com"  # To at least ignore really stupid crawlers
            email_to = "llamas" + "@" + "kbehrendt.com"
            send_mail(
                'Boxy submission by {}'.format(request.user.username),
                f"See title. Another submission. \n {content_str}",
                email_from,
                [email_to],
                fail_silently=True,
            )

            return render(request, 'boxy/quick_message.html',
                {'error': 'Submission successful',
                 'message': 'Feel free to shoot me an email to check if everything is in order.'})
        print('Form not valid')
    else:
        form = SubmissionForm(initial={'user': request.user.username})

    return render(request, 'boxy/submission.html',
                  {'form': form, 'error': 'Uploads regularly time out. Alternatively, send me a link to your submission to "boxy" @ "kbehrendt" . "com"!'})


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
    captcha = CaptchaField(label="I'm a human")

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
