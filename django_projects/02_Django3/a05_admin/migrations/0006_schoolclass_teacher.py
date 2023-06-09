# Generated by Django 3.2.19 on 2023-06-26 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a05_admin', '0005_alter_student_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='schoolclass_name')),
            ],
            options={
                'verbose_name': 'a05_schoolclass',
                'verbose_name_plural': 'a05_schoolclass',
                'db_table': 'a05_schoolclass',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='teacher_name')),
                ('school_class', models.ManyToManyField(to='a05_admin.SchoolClass', verbose_name='school_class')),
            ],
            options={
                'verbose_name': 'a05_teacher',
                'verbose_name_plural': 'a05_teacher',
                'db_table': 'a05_teacher',
            },
        ),
    ]
