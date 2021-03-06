# Generated by Django 4.0.2 on 2022-02-13 07:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bigyo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('szoveg', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Bigyo',
                'verbose_name_plural': 'Bigyók',
            },
        ),
        migrations.CreateModel(
            name='Feladat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nev', models.CharField(max_length=255)),
                ('url', models.URLField()),
            ],
            options={
                'verbose_name': 'Feladat',
                'verbose_name_plural': 'Feladat',
            },
        ),
        migrations.CreateModel(
            name='Hf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hatarido', models.DateTimeField()),
                ('mentoralando', models.BooleanField()),
                ('url', models.URLField()),
            ],
            options={
                'verbose_name': 'Házi feladat',
                'verbose_name_plural': 'Házi feladatok',
            },
        ),
        migrations.CreateModel(
            name='Temakor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nev', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Témakör',
                'verbose_name_plural': 'Témakörök',
            },
        ),
        migrations.CreateModel(
            name='Tartozik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feladat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APP.feladat')),
                ('temakor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APP.temakor')),
            ],
            options={
                'verbose_name': 'Témakör-Feladat reláció',
                'verbose_name_plural': 'Témakör-Feladat relációk',
            },
        ),
        migrations.CreateModel(
            name='Tanit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csoport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('tanar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tanár-Csoport reláció',
                'verbose_name_plural': 'Tanár-Csoport relációk',
            },
        ),
        migrations.CreateModel(
            name='Mo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('szoveg', models.CharField(max_length=255)),
                ('ido', models.DateTimeField(auto_now=True)),
                ('hf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APP.hf')),
            ],
            options={
                'verbose_name': 'Megoldás',
                'verbose_name_plural': 'Megoldások',
            },
        ),
        migrations.CreateModel(
            name='Mentoral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentor', to=settings.AUTH_USER_MODEL)),
                ('mentoree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentoree', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Mentorálás',
                'verbose_name_plural': 'Mentorálás',
            },
        ),
        migrations.CreateModel(
            name='Kituzes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ido', models.DateTimeField()),
                ('feladat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APP.feladat')),
                ('group', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('tanar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Kitűzés',
                'verbose_name_plural': 'Kitűzések',
            },
        ),
        migrations.AddField(
            model_name='hf',
            name='kituzes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APP.kituzes'),
        ),
        migrations.AddField(
            model_name='hf',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Git',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('platform', models.CharField(max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Git-User',
                'verbose_name_plural': 'Git-User',
            },
        ),
        migrations.CreateModel(
            name='Biralat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('szoveg', models.TextField()),
                ('itelet', models.CharField(max_length=100)),
                ('kozossegi_szolgalati_percek', models.IntegerField()),
                ('ido', models.DateTimeField(auto_now=True)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('mo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APP.mo')),
            ],
            options={
                'verbose_name': 'Bírálat',
                'verbose_name_plural': 'Bírálatok',
            },
        ),
    ]
