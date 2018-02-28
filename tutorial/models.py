# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class FormChoice(models.Model):
    slug = models.CharField(max_length=20)
    name = models.CharField(max_length=5000)
    description = models.CharField(max_length=5000)
    time = models.CharField(max_length=5000)
    question_amount = models.IntegerField()
    subject = models.CharField(max_length=5000)
    date = models.CharField(max_length=50)
    answers = models.TextField()
