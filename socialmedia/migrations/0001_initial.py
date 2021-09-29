# Generated by Django 3.2.7 on 2021-09-29 21:01

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
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(blank=True, max_length=140)),
                ('is_private', models.BooleanField(default=False)),
                ('image', models.ImageField(null=True, upload_to='images/profiles/')),
                ('followers', models.ManyToManyField(blank=True, related_name='followed_by', to='socialmedia.Profile')),
                ('following', models.ManyToManyField(blank=True, related_name='following_to', to='socialmedia.Profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=140)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(null=True, upload_to='images/posts/')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialmedia.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=140)),
                ('date', models.DateField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialmedia.post')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialmedia.profile')),
            ],
        ),
    ]
