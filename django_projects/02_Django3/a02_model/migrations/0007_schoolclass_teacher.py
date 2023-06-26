# Generated by Django 3.2.19 on 2023-06-08 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a02_model', '0006_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'a02_school_class',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('school_class', models.ManyToManyField(to='a02_model.SchoolClass')),
            ],
            options={
                'db_table': 'a02_teacher',
            },
        ),
    ]