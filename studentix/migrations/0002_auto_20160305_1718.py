# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-05 17:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studentix', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=100)),
                ('detail', models.CharField(max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='notice',
        ),
        migrations.AddField(
            model_name='notice',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentix.Course'),
        ),
    ]