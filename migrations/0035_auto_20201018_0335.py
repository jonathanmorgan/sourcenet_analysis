# Generated by Django 3.1.2 on 2020-10-18 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('context_text', '0032_auto_20191205_0356'),
        ('context_analysis', '0034_auto_20201018_0323'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reliability_names_eval',
            old_name='merged_from_article_datas',
            new_name='merged_from_ad',
        ),
        migrations.RenameField(
            model_name='reliability_names_eval',
            old_name='merged_to_article_datas',
            new_name='merged_to_ad',
        ),
    ]
