# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-25 23:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('context_text', '0012_auto_20160225_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reliability_Names',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.CharField(blank=True, max_length=255, null=True)),
                ('person_type', models.CharField(blank=True, max_length=255, null=True)),
                ('coder1_coder_id', models.IntegerField(blank=True, null=True)),
                ('coder1_detected', models.IntegerField(blank=True, null=True)),
                ('coder1_person_id', models.IntegerField(blank=True, null=True)),
                ('coder1_person_type', models.CharField(blank=True, max_length=255, null=True)),
                ('coder1_person_type_int', models.IntegerField(blank=True, null=True)),
                ('coder1_article_data_id', models.IntegerField(blank=True, null=True)),
                ('coder1_article_person_id', models.IntegerField(blank=True, null=True)),
                ('coder2_coder_id', models.IntegerField(blank=True, null=True)),
                ('coder2_detected', models.IntegerField(blank=True, null=True)),
                ('coder2_person_id', models.IntegerField(blank=True, null=True)),
                ('coder2_person_type', models.CharField(blank=True, max_length=255, null=True)),
                ('coder2_person_type_int', models.IntegerField(blank=True, null=True)),
                ('coder2_article_data_id', models.IntegerField(blank=True, null=True)),
                ('coder2_article_person_id', models.IntegerField(blank=True, null=True)),
                ('coder3_coder_id', models.IntegerField(blank=True, null=True)),
                ('coder3_detected', models.IntegerField(blank=True, null=True)),
                ('coder3_person_id', models.IntegerField(blank=True, null=True)),
                ('coder3_person_type', models.CharField(blank=True, max_length=255, null=True)),
                ('coder3_person_type_int', models.IntegerField(blank=True, null=True)),
                ('coder3_article_data_id', models.IntegerField(blank=True, null=True)),
                ('coder3_article_person_id', models.IntegerField(blank=True, null=True)),
                ('coder4_coder_id', models.IntegerField(blank=True, null=True)),
                ('coder4_detected', models.IntegerField(blank=True, null=True)),
                ('coder4_person_id', models.IntegerField(blank=True, null=True)),
                ('coder4_person_type', models.CharField(blank=True, max_length=255, null=True)),
                ('coder4_person_type_int', models.IntegerField(blank=True, null=True)),
                ('coder4_article_data_id', models.IntegerField(blank=True, null=True)),
                ('coder4_article_person_id', models.IntegerField(blank=True, null=True)),
                ('coder5_coder_id', models.IntegerField(blank=True, null=True)),
                ('coder5_detected', models.IntegerField(blank=True, null=True)),
                ('coder5_person_id', models.IntegerField(blank=True, null=True)),
                ('coder5_person_type', models.CharField(blank=True, max_length=255, null=True)),
                ('coder5_person_type_int', models.IntegerField(blank=True, null=True)),
                ('coder5_article_data_id', models.IntegerField(blank=True, null=True)),
                ('coder5_article_person_id', models.IntegerField(blank=True, null=True)),
                ('coder6_coder_id', models.IntegerField(blank=True, null=True)),
                ('coder6_detected', models.IntegerField(blank=True, null=True)),
                ('coder6_person_id', models.IntegerField(blank=True, null=True)),
                ('coder6_person_type', models.CharField(blank=True, max_length=255, null=True)),
                ('coder6_person_type_int', models.IntegerField(blank=True, null=True)),
                ('coder6_article_data_id', models.IntegerField(blank=True, null=True)),
                ('coder6_article_person_id', models.IntegerField(blank=True, null=True)),
                ('coder7_coder_id', models.IntegerField(blank=True, null=True)),
                ('coder7_detected', models.IntegerField(blank=True, null=True)),
                ('coder7_person_id', models.IntegerField(blank=True, null=True)),
                ('coder7_person_type', models.CharField(blank=True, max_length=255, null=True)),
                ('coder7_person_type_int', models.IntegerField(blank=True, null=True)),
                ('coder7_article_data_id', models.IntegerField(blank=True, null=True)),
                ('coder7_article_person_id', models.IntegerField(blank=True, null=True)),
                ('coder8_coder_id', models.IntegerField(blank=True, null=True)),
                ('coder8_detected', models.IntegerField(blank=True, null=True)),
                ('coder8_person_id', models.IntegerField(blank=True, null=True)),
                ('coder8_person_type', models.CharField(blank=True, max_length=255, null=True)),
                ('coder8_person_type_int', models.IntegerField(blank=True, null=True)),
                ('coder8_article_data_id', models.IntegerField(blank=True, null=True)),
                ('coder8_article_person_id', models.IntegerField(blank=True, null=True)),
                ('coder9_coder_id', models.IntegerField(blank=True, null=True)),
                ('coder9_detected', models.IntegerField(blank=True, null=True)),
                ('coder9_person_id', models.IntegerField(blank=True, null=True)),
                ('coder9_person_type', models.CharField(blank=True, max_length=255, null=True)),
                ('coder9_person_type_int', models.IntegerField(blank=True, null=True)),
                ('coder9_article_data_id', models.IntegerField(blank=True, null=True)),
                ('coder9_article_person_id', models.IntegerField(blank=True, null=True)),
                ('coder10_coder_id', models.IntegerField(blank=True, null=True)),
                ('coder10_detected', models.IntegerField(blank=True, null=True)),
                ('coder10_person_id', models.IntegerField(blank=True, null=True)),
                ('coder10_person_type', models.CharField(blank=True, max_length=255, null=True)),
                ('coder10_person_type_int', models.IntegerField(blank=True, null=True)),
                ('coder10_article_data_id', models.IntegerField(blank=True, null=True)),
                ('coder10_article_person_id', models.IntegerField(blank=True, null=True)),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='context_text.Article')),
                ('coder1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_names_coder1_set', to=settings.AUTH_USER_MODEL)),
                ('coder10', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_names_coder10_set', to=settings.AUTH_USER_MODEL)),
                ('coder2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_names_coder2_set', to=settings.AUTH_USER_MODEL)),
                ('coder3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_names_coder3_set', to=settings.AUTH_USER_MODEL)),
                ('coder4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_names_coder4_set', to=settings.AUTH_USER_MODEL)),
                ('coder5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_names_coder5_set', to=settings.AUTH_USER_MODEL)),
                ('coder6', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_names_coder6_set', to=settings.AUTH_USER_MODEL)),
                ('coder7', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_names_coder7_set', to=settings.AUTH_USER_MODEL)),
                ('coder8', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_names_coder8_set', to=settings.AUTH_USER_MODEL)),
                ('coder9', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_names_coder9_set', to=settings.AUTH_USER_MODEL)),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='context_text.Person')),
            ],
            options={
                'ordering': ['article', 'person_type', 'person'],
            },
        ),
        migrations.CreateModel(
            name='Reliability_Ties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.CharField(blank=True, max_length=255, null=True)),
                ('person_type', models.CharField(blank=True, max_length=255, null=True)),
                ('relation_type', models.CharField(blank=True, max_length=255, null=True)),
                ('relation_person_name', models.CharField(blank=True, max_length=255, null=True)),
                ('relation_person_type', models.CharField(blank=True, max_length=255, null=True)),
                ('coder1_mention_count', models.IntegerField(blank=True, null=True)),
                ('coder1_id_list', models.CharField(blank=True, max_length=255, null=True)),
                ('coder2_mention_count', models.IntegerField(blank=True, null=True)),
                ('coder2_id_list', models.CharField(blank=True, max_length=255, null=True)),
                ('coder3_mention_count', models.IntegerField(blank=True, null=True)),
                ('coder3_id_list', models.CharField(blank=True, max_length=255, null=True)),
                ('coder4_mention_count', models.IntegerField(blank=True, null=True)),
                ('coder4_id_list', models.CharField(blank=True, max_length=255, null=True)),
                ('coder5_mention_count', models.IntegerField(blank=True, null=True)),
                ('coder5_id_list', models.CharField(blank=True, max_length=255, null=True)),
                ('coder6_mention_count', models.IntegerField(blank=True, null=True)),
                ('coder6_id_list', models.CharField(blank=True, max_length=255, null=True)),
                ('coder7_mention_count', models.IntegerField(blank=True, null=True)),
                ('coder7_id_list', models.CharField(blank=True, max_length=255, null=True)),
                ('coder8_mention_count', models.IntegerField(blank=True, null=True)),
                ('coder8_id_list', models.CharField(blank=True, max_length=255, null=True)),
                ('coder9_mention_count', models.IntegerField(blank=True, null=True)),
                ('coder9_id_list', models.CharField(blank=True, max_length=255, null=True)),
                ('coder10_mention_count', models.IntegerField(blank=True, null=True)),
                ('coder10_id_list', models.CharField(blank=True, max_length=255, null=True)),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('coder1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_ties_coder1_set', to=settings.AUTH_USER_MODEL)),
                ('coder10', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_ties_coder10_set', to=settings.AUTH_USER_MODEL)),
                ('coder2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_ties_coder2_set', to=settings.AUTH_USER_MODEL)),
                ('coder3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_ties_coder3_set', to=settings.AUTH_USER_MODEL)),
                ('coder4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_ties_coder4_set', to=settings.AUTH_USER_MODEL)),
                ('coder5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_ties_coder5_set', to=settings.AUTH_USER_MODEL)),
                ('coder6', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_ties_coder6_set', to=settings.AUTH_USER_MODEL)),
                ('coder7', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_ties_coder7_set', to=settings.AUTH_USER_MODEL)),
                ('coder8', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_ties_coder8_set', to=settings.AUTH_USER_MODEL)),
                ('coder9', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_ties_coder9_set', to=settings.AUTH_USER_MODEL)),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_ties_from_set', to='context_text.Person')),
                ('relation_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reliability_ties_to_set', to='context_text.Person')),
            ],
            options={
                'ordering': ['person_type', 'person', 'relation_person'],
            },
        ),
    ]
