# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class FormChoice(models.Model):
    slug = models.CharField(max_length=20)
    name = models.CharField(max_length=5000)
    description = models.CharField(max_length=5000)
    time = models.CharField(max_length=5000)
    question_amount = models.IntegerField()
    answer_amount = models.IntegerField()
    subject = models.CharField(max_length=5000)
    date = models.CharField(max_length=50)
    answers = models.TextField()


class Student(models.Model):
    slug = models.CharField(max_length=50)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    year = models.CharField(max_length=100)

    _GRADE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6')
    )
    grade = models.CharField(max_length=100, choices=_GRADE)

    _LEVEL = (
        ('ประถม', 'ประถม'),
        ('มัธยม', 'มัธยม')
    )
    level = models.CharField(max_length=100, choices=_LEVEL)

    _ROOM = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4')
    )
    room = models.CharField(max_length=50, choices=_ROOM)

    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)

    def __unicode__(self):
        return u'{} {}'.format(self.firstname, self.lastname)


class Point(models.Model):
    slug = models.CharField(max_length=500, primary_key=True)
    point = models.CharField(max_length=20)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    form = models.ForeignKey(FormChoice, on_delete=models.CASCADE)
