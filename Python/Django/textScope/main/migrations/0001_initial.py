# Generated by Django 5.1.3 on 2024-11-29 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('values', models.TextField(help_text='Comma-seperated keywords for topics')),
                ('selected', models.BooleanField(default=False, help_text='Use this topic for analysis')),
            ],
        ),
    ]
