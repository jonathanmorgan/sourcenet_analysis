# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-14 16:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('context_analysis', '0007_auto_20160314_1636'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reliability_names_results',
            old_name='author_lookup_combined_alpha',
            new_name='author_lookup_alpha',
        ),
        migrations.RenameField(
            model_name='reliability_names_results',
            old_name='author_lookup_combined_percent',
            new_name='author_lookup_percent',
        ),
        migrations.RenameField(
            model_name='reliability_names_results',
            old_name='subject_lookup_combined_alpha',
            new_name='subject_lookup_alpha',
        ),
        migrations.RenameField(
            model_name='reliability_names_results',
            old_name='subject_lookup_combined_percent',
            new_name='subject_lookup_percent',
        ),
    ]
