from django.db import models
from django.contrib.auth.models import User


class Bigyo(models.Model):

    szoveg = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Bigyo'
        verbose_name_plural = 'Bigyók'

    def __str__(self):
        return self.szoveg


class Felhasznalo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ujtulajdonsag = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Felhasználó'
        verbose_name_plural = 'Felhasználók'

    def __str__(self):
        return str(self.user) + f' ({self.ujtulajdonsag})'
