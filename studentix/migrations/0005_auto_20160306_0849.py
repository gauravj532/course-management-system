# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-06 08:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('studentix', '0004_auto_20160306_0744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question_text',
        ),
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
        migrations.AddField(
            model_name='question',
            name='course',
            field=models.ForeignKey(default=datetime.datetime(2016, 3, 6, 8, 49, 12, 337968, tzinfo=utc), on_delete=django.db.models.deletion.CASCADE, to='studentix.Course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
