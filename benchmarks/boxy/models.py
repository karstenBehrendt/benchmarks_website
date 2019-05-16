from django.db import models


class Downloader(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
