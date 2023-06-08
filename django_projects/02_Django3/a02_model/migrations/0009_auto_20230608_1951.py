# Generated by Django 3.2.19 on 2023-06-08 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a02_model', '0008_auto_20230608_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='create time'),
        ),
        migrations.AddField(
            model_name='group',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='update time'),
        ),
        migrations.AddField(
            model_name='membership',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='create time'),
        ),
        migrations.AddField(
            model_name='membership',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='update time'),
        ),
        migrations.AddField(
            model_name='person',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='create time'),
        ),
        migrations.AddField(
            model_name='person',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='update time'),
        ),
    ]
