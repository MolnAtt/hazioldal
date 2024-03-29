# Generated by Django 4.1.2 on 2022-10-31 10:08

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dolgozat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nev', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('N', models.IntegerField()),
                ('M', models.IntegerField()),
                ('tanulok', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=1), size=50)),
                ('feladatok', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), size=200)),
                ('matrix', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=-1), size=50), size=200)),
                ('datum', models.DateTimeField()),
                ('suly', models.FloatField()),
                ('kettes_ponthatar', models.FloatField()),
                ('harmas_ponthatar', models.FloatField()),
                ('negyes_ponthatar', models.FloatField()),
                ('otos_ponthatar', models.FloatField()),
                ('duplaotos_ponthatar', models.FloatField()),
                ('egyketted_hatar', models.FloatField()),
                ('ketharmad_hatar', models.FloatField()),
                ('haromnegyed_hatar', models.FloatField()),
                ('negyotod_hatar', models.FloatField()),
                ('osztaly', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('tanar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Dolgozat',
                'verbose_name_plural': 'Dolgozatok',
            },
        ),
    ]
