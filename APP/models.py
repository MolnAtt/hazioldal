from inspect import classify_class_attrs
from msilib.schema import Class
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime, timezone

class Bigyo(models.Model):

    szoveg = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Bigyo'
        verbose_name_plural = 'Bigyók'

    def __str__(self):
        return self.szoveg


class Git(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    platform = models.CharField(max_length=15)
    
    class Meta:
        verbose_name = 'Git-User'
        verbose_name_plural = 'Git-User'

    def __str__(self):
        return f'{self.user}: {self.username}'


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
    nev = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'Témakör'
        verbose_name_plural = 'Témakörök'

    def __str__(self):
        return f'{self.nev}'


class Feladat(models.Model):
    nev = models.CharField(max_length=255)
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
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True)
    feladat = models.ForeignKey(Feladat, on_delete=models.CASCADE)
    ido = models.DateTimeField()
    
    class Meta:
        verbose_name = 'Kitűzés'
        verbose_name_plural = 'Kitűzések'

    def __str__(self):
        return f'{self.feladat} ({self.tanar}, {self.ido})'


class Hf(models.Model):
    kituzes = models.ForeignKey(Kituzes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hatarido = models.DateTimeField()
    mentoralando = models.BooleanField()
    
    class Meta:
        verbose_name = 'Házi feladat'
        verbose_name_plural = 'Házi feladatok'

    def __str__(self):
        return f'{self.kituzes.feladat} ({self.user}, {self.hatarido}{", mentoralando" if self.mentoralando else ""})'

    
    def fontos(self)->bool:
        """ egy hf fontos, ha van tennivaló van vele:
        - nincs repo hozzá
        - van repo de nincs beadva
        - be van adva de a legkésőbbi beadásra még nem jött bírálat
        - ... vagy létezik olyan bírálat, amely nem "Elfogadva".
        """
        a_repo = Repo.objects.filter(hf=self)
        if not a_repo.exists():
            return True
        a_megoldasok = Mo.objects.filter(repo=a_repo.first())
        if not a_megoldasok.exists():
            return True
        az_utolso_megoldas = a_megoldasok.order_by('ido').last()
        a_biralatok = Biralat.objects.filter(mo=az_utolso_megoldas)
        if not a_biralatok.exists or Biralat.van_elutasito(az_utolso_megoldas):
            return True
        return False

    def lista(a_user: User, predicate = lambda hf : hf) -> list:
        return list(map(lambda hf: {
                'cim': hf.kituzes.feladat.nev,
                'hatarido': hf.hatarido,
                'hatralevoido': (hf.hatarido-datetime.now(timezone.utc)).days,
                'temai': list(map(lambda t: t.temakor.nev, Tartozik.objects.filter(feladat=hf.kituzes.feladat))),
                'id':hf.id,
            }, filter(predicate, Hf.objects.filter(user=a_user))))


class Repo(models.Model):
    hf = models.ForeignKey(Hf, on_delete=models.CASCADE)
    url = models.URLField()
    
    class Meta:
        verbose_name = 'Repó'
        verbose_name_plural = 'Repók'


    def tulajdonosa(self, a_user:User) -> bool:
        return self.hf.user == a_user

    def __str__(self):
        return f'{self.hf.user}, {self.hf.kituzes.feladat}: {self.url}'

class Mo(models.Model):
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE, null=True)
    szoveg = models.CharField(max_length=255)
    ido = models.DateTimeField()
    
    class Meta:
        verbose_name = 'Megoldás'
        verbose_name_plural = 'Megoldások'

    def __str__(self):
        return f'{self.hf.user}, {self.hf.kituzes.feladat} ({self.ido}):{self.url})'


class Biralat(models.Model):
    mo = models.ForeignKey(Mo, on_delete=models.CASCADE)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    szoveg = models.TextField()
    itelet = models.CharField(max_length=100)
    kozossegi_szolgalati_orak = models.IntegerField()
    ido = models.DateTimeField()
    
    class Meta:
        verbose_name = 'Bírálat'
        verbose_name_plural = 'Bírálatok'

    def __str__(self):
        return f'{self.mentor}, {self.itelet}: {self.szoveg if len(self.szoveg)<=100 else (self.szoveg[:100]+"...")} ({self.mo.hf.kituzes.feladat}, {self.mo.hf.user})'
        

    def van_elutasito(a_mo: Mo) -> bool:
        for biralat in Biralat.objects.filter(mo=a_mo):
            if biralat.itelet != "Elfogadva":
                return True
        return False

