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
            content_str = "\n".join([f"{field}: {value}" for field, value in form.cleaned_data.items()])
            print(content_str)

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
    context['benchmark_name'] = 'Lane Approximations'
    context['benchmark_short'] = 'Because curves can be easier to handle than a few thousand pixels'

    # paper metrics
    context['metric_name'] = "Mean absolute distance"
    context['metric_description'] = "The original dataset metric. To get a feeling for the overall accuracy of the detector for each annotated lane segment."
    context['results'] = [
        {'Name': 'VSA SP', 'All': '17.88', 'l1': '32.62', 'l0': '8.74', 'r0': '9.95', 'r1': '25.93', 'Comment': "Trained on train and valid sets"},
        {'Name': 'VSA SP', 'All': '18.47', 'l1': '32.84', 'l0': '8.57', 'r0': '11.56', 'r1': '26.51', 'Comment': "Trained on training set only"},
        {'Name': 'VSA', 'All': '19.00', 'l1': '34.77', 'l0': '8.74', 'r0': '10.79', 'r1': '27.84', 'Comment': ""},
        {'Name': 'Simple Mean Baseline', 'All': '31.00', 'l1': '33.78', 'l0': '26.34', 'r0': '30.24', 'r1': '34.75', 'Comment': "Within github repo"},
    ]
    context['keys'] = list(context['results'][0].keys())

    # culane metrics
    context['metric_name2'] = "CULane Metrics"
    context['metric_description2'] = "Accuracy metrics for detected lanes based on 30 pixel accuracy and an IoU greater or equal to 0.5"
    """ Empty entry block
            {'Name': '', 'TP': '', 'FP': '', 'FN': '', 'Precision': '', 'Recall': '', 'F1': '', 'Comment': ""},
    """
    context['results2'] = [
            {'Name': 'LaneAF', 'TP': '71793', 'FP': '2291', 'FN': '3576', 'Precision': '0.9691', 'Recall': '0.9526', 'F1': '0.9601', 'Comment': "Code https://github.com/sel118/LaneAF, paper http://cvrr.ucsd.edu/publications/2021/LaneAF.pdf, 10 fps"},  
            {'Name': 'RCLaneDet-L', 'TP': '71964', 'FP': '2385', 'FN': '3405', 'Precision': '0.9679', 'Recall': '0.9548', 'F1': '0.9613', 'Comment': ""},
            {'Name': 'RCLaneDet-S', 'TP': '71915', 'FP': '2458', 'FN': '3454', 'Precision': '0.9670', 'Recall': '0.9542', 'F1': '0.9605', 'Comment': ""},
            {'Name': 'RCLaneDet-M', 'TP': '71941', 'FP': '2513', 'FN': '3428', 'Precision': '0.9662', 'Recall': '0.9545', 'F1': '0.9603', 'Comment': ""},
            {'Name': 'BezierLaneNet (ResNet-34)', 'TP': '71191', 'FP': '3050', 'FN': '4178', 'Precision': '0.9589', 'Recall': '0.9446', 'F1': '0.9517', 'Comment': "Code and models will be at: https://github.com/voldemortX/pytorch-auto-drive, Paper: TBD."},
            {'Name': 'SCNN VGG16', 'TP': '71425', 'FP': '3315', 'FN': '3944', 'Precision': '0.9556', 'Recall': '0.9477', 'F1': '0.9516', 'Comment': "Code and models: https://github.com/voldemortX/pytorch-auto-drive, Paper: https://ojs.aaai.org/index.php/AAAI/article/view/12301."},
            {'Name': 'BezierLaneNet (ResNet-18)', 'TP': '70946', 'FP': '3180', 'FN': '4423', 'Precision': '0.9571', 'Recall': '0.9413', 'F1': '0.9491', 'Comment': "Code and models will be at: https://github.com/voldemortX/pytorch-auto-drive, Paper: TBD."},
            {'Name': 'PointLaneNet Sup', 'TP': '71460', 'FP': '3636', 'FN': '3729', 'Precision': '0.9517', 'Recall': '0.9505', 'F1': '0.9511', 'Comment': ""},
            {'Name': 'Baseline ERFNet', 'TP': '71235', 'FP': '3673', 'FN': '4134', 'Precision': '0.9510', 'Recall': '0.9451', 'F1': '0.9480', 'Comment': "Code and models:  https://github.com/voldemortX/pytorch-auto-drive"},
            {'Name': 'Baseline VGG16', 'TP': '70824', 'FP': '3380', 'FN': '4545', 'Precision': '0.9544', 'Recall': '0.9397', 'F1': '0.9470', 'Comment': "Code and models:  https://github.com/voldemortX/pytorch-auto-drive, Paper: https://ojs.aaai.org/index.php/AAAI/article/view/12301."},
            {'Name': 'BGCA Remote', 'TP': '71135', 'FP': '4124', 'FN': '4234', 'Precision': '0.9452', 'Recall': '0.9438', 'F1': '0.9445', 'Comment': ""},
            {'Name': 'BGCA Local', 'TP': '71294', 'FP': '4550', 'FN': '4075', 'Precision': '0.9400', 'Recall': '0.9459', 'F1': '0.9430', 'Comment': ""},
            {'Name': 'SCNN ResNet34', 'TP': '71141', 'FP': '4455', 'FN': '4228', 'Precision': '0.9411', 'Recall': '0.9439', 'F1': '0.9425', 'Comment': "Code and models:  https://github.com/voldemortX/pytorch-auto-drive"},
            {'Name': 'SCNN ERFNet', 'TP': '71329', 'FP': '5050', 'FN': '4040', 'Precision': '0.9339', 'Recall': '0.9464', 'F1': '0.9401', 'Comment': "Code and models:  https://github.com/voldemortX/pytorch-auto-drive"},
            {'Name': 'MSCA Resnet34', 'TP': '68474', 'FP': '2204', 'FN': '6895', 'Precision': '0.9688', 'Recall': '0.9085', 'F1': '0.9377', 'Comment': ""},
            {'Name': 'MSCA Resnet19', 'TP': '68493', 'FP': '2283', 'FN': '6876', 'Precision': '0.9677', 'Recall': '0.9088', 'F1': '0.9373', 'Comment': ""},
            {'Name': 'LaneATT (ResNet-34)', 'TP': '68495', 'FP': '2273', 'FN': '6874', 'Precision': '0.9679', 'Recall': '0.9088', 'F1': '0.9374', 'Comment': "Code and models:  https://github.com/lucastabelini/LaneATT."},
            {'Name': 'LaneATT (ResNet-122)', 'TP': '68190', 'FP': '2239', 'FN': '7179', 'Precision': '0.9682', 'Recall': '0.9047', 'F1': '0.9354', 'Comment': "Code and models:  https://github.com/lucastabelini/LaneATT."},
            {'Name': 'LaneATT (ResNet-18)', 'TP': '68012', 'FP': '2161', 'FN': '7357', 'Precision': '0.9692', 'Recall': '0.9024', 'F1': '0.9346', 'Comment': "Code and models:  https://github.com/lucastabelini/LaneATT."},
            {'Name': 'Baseline ResNet34', 'TP': '71046', 'FP': '5667', 'FN': '4320', 'Precision': '0.9261', 'Recall': '0.9427', 'F1': '0.9343', 'Comment': "Code and models: https://github.com/voldemortX/pytorch-auto-drive, Paper: https://ojs.aaai.org/index.php/AAAI/article/view/12301."},  
            {'Name': 'PointLaneNeti Ssl', 'TP': '63794', 'FP': '4109', 'FN': '11575', 'Precision': '0.9395', 'Recall': '0.8464', 'F1': '0.8905', 'Comment': ""},
            {'Name': 'PolyLaneNet', 'TP': '66272', 'FP': '8302', 'FN': '9097', 'Precision': '0.8887', 'Recall': '0.8793', 'F1': '0.8840', 'Comment': "Code and models:  https://github.com/lucastabelini/PolyLaneNet."},
            {'Name': 'PointLaneNet Base', 'TP': '64953', 'FP': '11246', 'FN': '10416', 'Precision': '0.8524', 'Recall': '0.8618', 'F1': '0.8571', 'Comment': ""},
            {'Name': 'Mean Baseline', 'TP': '917', 'FP': '82799', 'FN': '74452', 'Precision': '0.0110', 'Recall': '0.0122', 'F1': '0.0115', 'Comment': "Not useful as baseline"},
    ]
    context['keys2'] = list(context['results2'][0].keys())
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
