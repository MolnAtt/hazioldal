# Generated by Django 4.1.2 on 2023-06-27 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('APP', '0011_haladek_kerelem_egyes'),
    ]

    operations = [
        migrations.CreateModel(
            name='HaziCsoport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ev', models.IntegerField()),
                ('szekcio', models.CharField(max_length=8)),
                ('tagozat', models.CharField(max_length=8)),
                ('egyeb', models.CharField(max_length=64)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
            options={
                'verbose_name': 'Csoport',
                'verbose_name_plural': 'Csoportok',
            },
        ),
    ]