# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-12 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20161229_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='upvoted_blogs',
            field=models.ManyToManyField(db_table='blog_user_blogdata', related_name='upvoted_blogs', to='blog.BlogData'),
        ),
    ]
