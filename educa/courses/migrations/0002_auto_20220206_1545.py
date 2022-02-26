# Generated by Django 3.1.5 on 2022-02-06 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='slug',
            field=models.SlugField(default='slug', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
