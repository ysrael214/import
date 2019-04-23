# Generated by Django 2.2 on 2019-04-23 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Course Name')),
                ('code', models.CharField(max_length=10, verbose_name='Course Code')),
                ('number', models.CharField(max_length=10, verbose_name='Course Number')),
                ('title', models.CharField(max_length=50, verbose_name='Course Title')),
                ('description', models.TextField(blank=True, verbose_name='Course Description')),
                ('old_curr', models.BooleanField(default=False, verbose_name='Pre-2018 Curriculum Exclusive?')),
            ],
        ),
    ]
