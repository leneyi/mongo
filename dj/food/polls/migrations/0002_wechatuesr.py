# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-13 07:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WechatUesr',
            fields=[
                ('openid', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('nickname', models.CharField(max_length=200)),
            ],
        ),
    ]