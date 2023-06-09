# Generated by Django 3.2.19 on 2023-06-08 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a02_model', '0004_auto_20230608_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'a02_place',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('place', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='a02_model.place')),
                ('serves_hot_dog', models.BooleanField(default=True)),
                ('serves_pizza', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'a02_restaurant',
            },
        ),
        migrations.CreateModel(
            name='Waiter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a02_model.restaurant')),
            ],
            options={
                'db_table': 'a02_waiter',
            },
        ),
    ]
