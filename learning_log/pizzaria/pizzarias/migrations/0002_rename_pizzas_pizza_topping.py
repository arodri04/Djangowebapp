# Generated by Django 5.1.3 on 2024-11-14 16:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzarias', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pizzas',
            new_name='Pizza',
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizzarias.pizza')),
            ],
            options={
                'verbose_name_plural': 'toppings',
            },
        ),
    ]
