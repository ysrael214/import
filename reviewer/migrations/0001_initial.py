# Generated by Django 3.0.4 on 2020-03-31 21:22

from django.conf import settings
import django.contrib.auth.models
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import reviewer.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('userID', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Username')),
                ('first_name', models.CharField(max_length=30, verbose_name='First Name')),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Middle Name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last Name')),
                ('suffix', models.CharField(blank=True, max_length=10, null=True, verbose_name='Suffix')),
                ('studentnum', models.PositiveIntegerField(null=True, verbose_name='Student Number')),
                ('show_studentnum', models.BooleanField(default=True, verbose_name='Show Student Number')),
                ('email', models.EmailField(max_length=60, verbose_name='E-mail')),
                ('show_email', models.BooleanField(default=True, verbose_name='Show E-mail')),
                ('course', models.CharField(max_length=60, verbose_name='Course/Degree Program')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Is SuperUser?')),
                ('exp', models.PositiveIntegerField(default=0, verbose_name='Experience Points')),
                ('prof_picID', models.CharField(blank=True, default=None, max_length=40, null=True, verbose_name='Prof Pic ID')),
                ('dark_mode', models.BooleanField(default=False, verbose_name='Dark Mode')),
                ('notifications', models.BooleanField(default=True, verbose_name='Notifications')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=150)),
                ('image', models.ImageField(blank=True, null=True, upload_to=reviewer.models.post_uploadto, verbose_name='Image')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Posted')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Course Name')),
                ('code', models.CharField(max_length=10, verbose_name='Course Code')),
                ('number', models.CharField(max_length=10, verbose_name='Course Number')),
                ('number_len', models.PositiveSmallIntegerField(default=1)),
                ('title', models.CharField(max_length=50, verbose_name='Course Title')),
                ('description', models.TextField(blank=True, verbose_name='Course Description')),
                ('old_curr', models.BooleanField(default=False, verbose_name='Pre-2018 Curriculum Exclusive?')),
                ('visible', models.BooleanField(default=True, verbose_name='Visible?')),
                ('lastupdated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last Updated')),
                ('image', models.ImageField(blank=True, null=True, upload_to=reviewer.models.course_uploadto, verbose_name='Cover Photo')),
                ('coreqs', models.ManyToManyField(blank=True, default=None, related_name='creq', to='reviewer.Course')),
                ('prereqs', models.ManyToManyField(blank=True, default=None, related_name='preq', to='reviewer.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to=reviewer.models.language_uploadto, verbose_name='Icon')),
                ('color', models.CharField(default='868686', max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('verified', models.BooleanField(default=False, verbose_name='Verified?')),
                ('verifier', models.CharField(max_length=50)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewer.Course')),
                ('ex_lang', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviewer.Language')),
                ('prereq_lesson', models.ManyToManyField(blank=True, default=None, related_name='_lesson_prereq_lesson_+', to='reviewer.Lesson')),
            ],
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('body', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('link', models.CharField(max_length=100)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewer.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_code', models.TextField()),
                ('qtype', models.CharField(max_length=50)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewer.Lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('custom_code', models.TextField()),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewer.Lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewer.Comment')),
                ('user_attr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LessonStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_made', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date')),
                ('skips', models.PositiveSmallIntegerField(default=0)),
                ('mistakes', models.PositiveSmallIntegerField(default=0)),
                ('lesson_attr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewer.Course')),
                ('user_attr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='course_attr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviewer.Course'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_attr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BugReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Title')),
                ('body', models.CharField(max_length=300, verbose_name='Body')),
                ('status', models.PositiveSmallIntegerField(default=0, verbose_name='Status')),
                ('lastupdated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last Updated')),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('body', django.contrib.postgres.fields.jsonb.JSONField()),
                ('image', models.ImageField(blank=True, null=True, upload_to=reviewer.models.announcement_uploadto, verbose_name='Image')),
                ('datepost', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Posted')),
                ('poster', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='importuser',
            name='fave_lang',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviewer.Language', verbose_name='Favorite Language'),
        ),
        migrations.AddField(
            model_name='importuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='importuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
