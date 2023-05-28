# Generated by Django 2.2.28 on 2023-05-28 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0002_auto_20230528_1831'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='the name')),
                ('age', models.IntegerField(verbose_name='the age')),
                ('email', models.EmailField(max_length=254, verbose_name='the email')),
            ],
        ),
    ]
