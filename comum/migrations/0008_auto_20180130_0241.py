# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-30 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comum', '0007_auto_20180130_0235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='curtida',
        ),
        migrations.AddField(
            model_name='perfil',
            name='curtida',
            field=models.ManyToManyField(blank=True, related_name='curtidas', to='comum.Job'),
        ),
    ]
