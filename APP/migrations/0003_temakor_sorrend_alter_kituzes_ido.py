# Generated by Django 4.0.2 on 2022-02-19 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0002_delete_bigyo'),
    ]

    operations = [
        migrations.AddField(
            model_name='temakor',
            name='sorrend',
            field=models.CharField(default='-', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='kituzes',
            name='ido',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
