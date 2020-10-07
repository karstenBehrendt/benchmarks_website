import datetime
import os
import requests

from django import forms
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.forms import ModelForm
from django.http import HttpResponse

from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader

from captcha.fields import CaptchaField

from boxy.models import Submission


def index(request):
    index_template = loader.get_template('llamas/index.html')
    context = dict()
    return HttpResponse(index_template.render(context, request))


@login_required(login_url='../llamas/login')
def download(request):
    europe_server = 'http://5.9.71.146'
    current_simlink = 'vlyJctVXJu8Hfw'
    index_template = loader.get_template('llamas/download_links.html')
    context = {'europe_server': europe_server, 'current_simlink': current_simlink}
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
                'Llamas submission by {}'.format(request.user.username),
                f"See title. Another submission. \n {content_str}",
                 email_from,
                [email_to],
                fail_silently=True,
            )

            return render(request, 'llamas/quick_message.html',
                {'error': 'Submission successful',
                 'message': 'Feel free to shoot me an email to check if everything is in order.'})
        print('Form not valid')
    else:
        form = SubmissionForm(initial={'user': request.user.username})

    return render(request, 'llamas/submission.html',
                  {'form': form, 'error': 'Uploads seem to time out regularly. Alternatively send a link to your submission to "llamas" @ "kbehrendt" . "com"!'})


def contact(request):
    index_template = loader.get_template('llamas/contact.html')
    context = dict()
    return HttpResponse(index_template.render(context, request))


def benchmarks(request):
    # TODO Add links to other benchmarks here
    index_template = loader.get_template('llamas/benchmarks.html')
    context = dict()
    return HttpResponse(index_template.render(context, request))


def labelling(request):
    # TODO Add links to other benchmarks here
    index_template = loader.get_template('llamas/labelling.html')
    context = dict()
    return HttpResponse(index_template.render(context, request))


def benchmark_binary(request):
    index_template = loader.get_template('llamas/benchmark_base.html')
    context = dict()
    # TODO Move into database once there are more results, make it sortable
    context['results'] = [
            {'Name': 'GAC Baseline 1', 'AP': '0.778', 'Corner Precision': '0.748', 'Corner Recall': '0.307',
             'Runtime': '0.05 s', 'Environment': 'PyTorch, Tesla V100',
             'Code': 'Not public yet',
             'Paper': 'Not public yet', 'External data': 'No', 'Special comment': ''},
            {'Name': 'Simple Baseline', 'AP': '0.434', 'Corner Precision': '0.546', 'Corner Recall': '0.450',
             'Runtime': '0.044 s', 'Environment': 'cuDNN, Nvidia GeForce 1080 Ti',
             'Code': '<a href="https://github.com/karstenBehrendt/unsupervised_llamas/tree/master/simple_baseline"> code </a>',
             'Paper': '<a href="https://unsupervised-llamas.com">paper</a>', 'External data': 'No', 'Special comment': ''}
    ]
    context['keys'] = list(context['results'][0].keys())
    context['benchmark_name'] = 'Binary Lane Marker Segmentation'
    context['benchmark_short'] = 'Decide whether a pixel belongs to a lane marker or not'
    return HttpResponse(index_template.render(context, request))


def benchmark_multi(request):
    index_template = loader.get_template('llamas/benchmark_base.html')
    context = dict()
    # TODO Move into database once there are more results, make it sortable
    # NOTE Can be a lot prettier by going away from the generic table
    context['results'] = [
            {'Name': 'GAC Baseline 1', 'mAP': '0.761', 'ap BG': '.999', 'ap L1': '0.432',
             'ap L0': '0.941', 'ap R0': '0.925', 'ap R1': '0.744',
             'Runtime': '0.05 s', 'Environment': 'PyTorch, Tesla 100',
             'Code': 'Not public yet',
             'Paper': 'Not public yet', 'External data': 'No', 'Comment': ''},
            {'Name': 'ENet-SAD-Simple', 'mAP': '0.635', 'ap BG': '.999', 'ap L1': '0.266',
             'ap L0': '0.896', 'ap R0': '0.880', 'ap R1': '0.498',
             'Runtime': '0.013 s', 'Environment': 'Torch',
             'Code': '<a href="https://github.com/cardwing/Codes-for-Lane-Detection"> code </a>',
             'Paper': '<a href="https://arxiv.org/abs/1908.00821">paper</a>', 'External data': 'No', 'Comment': ''},
            {'Name': 'Simple Baseline', 'mAP': '0.500', 'ap BG': '.999', 'ap L1': '0.211',
             'ap L0': '0.751', 'ap R0': '0.706', 'ap R1': '0.335',
             'Runtime': '0.044 s', 'Environment': 'cuDNN, Nvidia GeForce 1080 Ti',
             'Code': '<a href="https://github.com/karstenBehrendt/unsupervised_llamas/tree/master/simple_baseline"> code </a>',
             'Paper': '<a href="https://unsupervised-llamas.com">paper</a>', 'External data': 'No', 'Comment': ''}
    ]
    context['keys'] = list(context['results'][0].keys())
    context['benchmark_name'] = 'Multi-class Lane Marker Segmentation'
    context['benchmark_short'] = 'Decide whether a pixel belongs to a marker and assign it to a lane'
    return HttpResponse(index_template.render(context, request))


def benchmark_splines(request):
    index_template = loader.get_template('llamas/benchmark_base.html')
    context = dict()
    # TODO results
    context['results'] = [{'Name': 'Simple Mean Baseline', 'All': '31.00', 'l1': '33.78', 'l0': '26.34', 'r0': '30.24', 'r1': '34.75', 'Comment': "Within github repo"}]
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
                return redirect('llamas_download')
        else:
            error = '--> You need to accept the license <--'
    else:
        form = SignUpForm()

    return render(request, 'llamas/signup.html',
                  {'form': form, 'error': error, 'form_name': 'Register'})
