# Generated by Django 3.1.5 on 2021-01-28 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summarizer', '0003_add_sites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
