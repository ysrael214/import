# Generated by Django 3.0.5 on 2020-04-28 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewer', '0004_auto_20200423_0457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='qtype',
            field=models.CharField(max_length=10),
        ),
    ]
