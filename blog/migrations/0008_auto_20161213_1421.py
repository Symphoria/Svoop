# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-13 08:51
from __future__ import unicode_literals

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20161213_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=cloudinary.models.CloudinaryField(default='image', max_length=255),
        ),
    ]