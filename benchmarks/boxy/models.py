from django.db import models


class Downloader(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)


class Submission(models.Model):
    user = models.CharField('User name', max_length=100)
    model_name = models.CharField('Model name', max_length=100)
    speed = models.FloatField('Inference time in seconds')  # in seconds
    env = models.CharField('Software and Hardware Environment', max_length=100, blank=True)
    external_used = models.CharField(
        'Was data that was not part of this dataset used? (No | Yes | Only)',
        choices=[('No', 'No'), ('Yes', 'Yes'), ('Only', 'Only')],
        max_length=4)
    paper = models.CharField('Link to paper', max_length=100, blank=True)
    repo = models.CharField('Link to repo', max_length=100, blank=True)
    comments_private = models.CharField(
        'Private comments for processing the submission', max_length=500, blank=True)
    comments_public = models.CharField(
        'Public comment about the submission', max_length=500, blank=True)
    inference_file = models.FileField('Inference results', upload_to='data/')
