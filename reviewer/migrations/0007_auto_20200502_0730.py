# Generated by Django 3.0.5 on 2020-05-01 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviewer', '0006_auto_20200429_0706'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='lesson',
            name='unique course-order',
        ),
    ]
