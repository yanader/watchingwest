# Generated by Django 4.2 on 2023-09-19 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('westaway', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=64)),
            ],
        ),
    ]
