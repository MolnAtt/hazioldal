# Generated by Django 4.0.2 on 2022-03-13 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0005_alter_git_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='git',
            name='platform',
            field=models.CharField(max_length=255),
        ),
    ]