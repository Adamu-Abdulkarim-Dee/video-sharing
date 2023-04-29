# Generated by Django 4.1 on 2023-04-21 01:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('video', models.FileField(upload_to='videos')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('banner', models.ImageField(upload_to='banner')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReportVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('this_is', models.CharField(choices=[('Pornography', 'Pornography'), ('Graphic Violence', 'Graphic Violence'), ('Predators Behavior', 'Predators Behavior')], max_length=100)),
                ('more_information', models.TextField(max_length=400)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.video')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(default='static/dafault.jpg', upload_to='profile-image')),
                ('twitter', models.URLField(blank=True, null=True, unique=True)),
                ('website', models.URLField(blank=True, null=True, unique=True)),
                ('linkedln', models.URLField(blank=True, null=True, unique=True)),
                ('country', models.CharField(blank=True, max_length=70, null=True)),
                ('about', models.TextField(blank=True, max_length=700, null=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]