# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-06 11:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentix', '0011_auto_20160306_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='send_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]