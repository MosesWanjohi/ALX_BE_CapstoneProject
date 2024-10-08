# Generated by Django 5.1 on 2024-09-27 21:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('media', models.ImageField(blank=True, null=True, upload_to='media')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('post_type', models.CharField(choices=[('listing', 'Listing'), ('event', 'Event'), ('blog post', 'Blog Post'), ('market analysis', 'Market Analysis')], default='listing', max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
