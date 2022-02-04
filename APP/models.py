from inspect import classify_class_attrs
from msilib.schema import Class
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User, Group


class Bigyo(models.Model):

    szoveg = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Bigyo'
        verbose_name_plural = 'Bigyók'

    def __str__(self):
        return self.szoveg


class Tanit(models.Model):
    tanar = models.ForeignKey(User, on_delete=models.CASCADE)
    csoport = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Tanár-Csoport reláció'
        verbose_name_plural = 'Tanár-Csoport relációk'

    def __str__(self):
        return f'{self.tanar} --- {self.csoport}'


class Mentoral(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor')
    mentoree = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentoree')
    
    class Meta:
        verbose_name = 'Mentorálás'
        verbose_name_plural = 'Mentorálás'

    def __str__(self):
        return f'{self.mentor} --- {self.mentoree}'



class Temakor(models.Model):
    nev = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Témakör'
        verbose_name_plural = 'Témakörök'

    def __str__(self):
        return f'{self.nev}'


class Feladat(models.Model):
    url = models.URLField()
    
    class Meta:
        verbose_name = 'Feladat'
        verbose_name_plural = 'Feladat'

    def __str__(self):
        return f'{self.nev}'


class Tartozik(models.Model):
    temakor = models.ForeignKey(Temakor, on_delete=models.CASCADE)
    feladat = models.ForeignKey(Feladat, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Témakör-Feladat reláció'
        verbose_name_plural = 'Témakör-Feladat relációk'

    def __str__(self):
        return f'{self.temakor} --- {self.feladat}'



class Kituzes(models.Model):
    tanar = models.ForeignKey(User, on_delete=models.CASCADE)
    feladat = models.ForeignKey(Feladat, on_delete=models.CASCADE)
    ido = models.DateTimeField()
    
    class Meta:
        verbose_name = 'Kitűzés'
        verbose_name_plural = 'Kitűzések'

    def __str__(self):
        return f'{self.feladat} ({self.tanar}, {self.ido})'


class Hf(models.Model):
    kituzes = models.ForeignKey(Kituzes, on_delete=models.CASCADE)
    felhasznalo = models.ForeignKey(User, on_delete=models.CASCADE)
    hatarido = models.DateTimeField()
    mentoralando = models.BooleanField()
    
    class Meta:
        verbose_name = 'Házi feladat'
        verbose_name_plural = 'Házi feladatok'

    def __str__(self):
        return f'{self.kituzes.feladat} ({self.felhasznalo}, {self.hatarido}{", mentoralando" if self.mentoralando else ""})'

class Mo(models.Model):
    hf = models.ForeignKey(Hf, on_delete=models.CASCADE)
    url = models.URLField()
    ido = models.DateTimeField()
    
    class Meta:
        verbose_name = 'Megoldás'
        verbose_name_plural = 'Megoldások'

    def __str__(self):
        return f'{self.hf.felhasznalo}, {self.hf.kituzes.feladat} ({self.ido}):{self.url})'
        

class Biralat(models.Model):
    mo = models.ForeignKey(Mo, on_delete=models.CASCADE)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    szoveg = models.TextField()
    itelet = models.CharField(max_length=100)
    kozossegi_szolgalati_orak = models.IntegerField()
    ido = models.DateTimeField()
    
    class Meta:
        verbose_name = 'Megoldás'
        verbose_name_plural = 'Megoldások'

    def __str__(self):
        return f'{self.hf.felhasznalo}, {self.hf.kituzes.feladat} ({self.ido}):{self.url})'
        

