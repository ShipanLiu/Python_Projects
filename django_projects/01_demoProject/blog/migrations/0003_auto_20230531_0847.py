# Generated by Django 2.2.28 on 2023-05-31 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20230530_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.CharField(max_length=10, verbose_name='related uid'),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.CharField(max_length=10, verbose_name='related uid'),
        ),
    ]
