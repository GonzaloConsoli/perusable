# Generated by Django 3.2.9 on 2022-08-06 14:12

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20220806_1401'),
    ]

    operations = [
        # migrations.AddIndex(
        #     model_name='wine',
        #     index=django.contrib.postgres.indexes.GinIndex(fields=['description', 'winery', 'variety'], name='desc_winery_variety_gin_idx', opclasses=['gin_trgm_ops', 'gin_trgm_ops', 'gin_trgm_ops']),
        # ),
    ]
