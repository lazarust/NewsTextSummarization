# Generated by Django 3.1.5 on 2021-01-28 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summarizer', '0004_auto_20210128_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_link',
            field=models.CharField(max_length=300, unique=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='headline',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
