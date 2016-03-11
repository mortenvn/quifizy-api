# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-11 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='songs',
            field=models.ManyToManyField(to='api.Song'),
        ),
    ]