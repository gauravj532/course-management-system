# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-06 10:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentix', '0006_question_question_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='score',
        ),
    ]
