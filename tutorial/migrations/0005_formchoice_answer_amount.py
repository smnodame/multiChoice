# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-15 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0004_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='formchoice',
            name='answer_amount',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
    ]