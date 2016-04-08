# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-14 17:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_round_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.Round'),
        ),
        migrations.AlterField(
            model_name='round',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='quiz.Game'),
        ),
    ]