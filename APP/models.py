# from inspect import classify_class_attrs
# from msilib.schema import Class
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime, timezone

allapotszotar = {
    'NINCS_REPO' : 'uj',
    'NINCS_MO' : 'uj',
    'NINCS_BIRALAT' : 'biral',
    'VAN_NEGATIV_BIRALAT': 'uj',
    'MINDEN_BIRALAT_POZITIV' : 'kesz',
}

class Git(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'Git-profil'
        verbose_name_plural = 'Git-profilok'

    def __str__(self):
        return f'{self.user}: {self.username}'
    
    def letrehozasa_mindenkinek_ha_meg_nincs() -> str:
        db = 0
        for a_user in User.objects.all():
            a_git = Git.objects.filter(user = a_user).first()
            if a_git == None:
                Git.objects.create(
                    user = a_user,
                    username = '-',
                    email = a_user.email,
                    platform = 'https://github.com/',
                    )    
                db += 1
        return f'{db} db új git user lett létrehozva, és így már {Git.objects.count()} db git user van'

    




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

    def ja(a_mentor: User, a_mentoralt: User) -> bool:
        return Mentoral.objects.filter(mentor=a_mentor, mentoree=a_mentoralt).exists()

    def tjai(a_mentor: User):
        return list(map(lambda m: m.mentoree, Mentoral.objects.filter(mentor=a_mentor)))

    def oi(a_mentoralt: User):
        return list(map(lambda m: m.mentor, Mentoral.objects.filter(mentoree=a_mentoralt)))

    



class Temakor(models.Model):
    sorrend = models.CharField(max_length=255)
    nev = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'Témakör'
        verbose_name_plural = 'Témakörök'

    def __str__(self):
        return f'{self.nev} ({self.sorrend})'


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
    ido = models.DateTimeField(auto_now = True)
    
    class Meta:
        verbose_name = 'Kitűzés'
        verbose_name_plural = 'Kitűzések'

    def __str__(self):
        return f'{self.feladat} ({self.tanar}, {self.ido})'


class Hf(models.Model):
    kituzes = models.ForeignKey(Kituzes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hatarido = models.DateTimeField()
    mentoralando = models.BooleanField(default=True)
    url = models.URLField(default="https://github.com/")
    
    class Meta:
        verbose_name = 'Házi feladat'
        verbose_name_plural = 'Házi feladatok'

    def __str__(self):
        return f'{self.kituzes.feladat} ({self.user}, {self.hatarido}{", mentoralando" if self.mentoralando else ""})'

    @property
    def tulajdonosa(a_hf):
        return f"{a_hf.user.last_name} {a_hf.user.first_name}"

    def sajat_hazijaim(a_user):
        return list(Hf.objects.filter(user=a_user))

    def mentoraltak_hazijainak_unioja(mentor:User) -> list:
        lista = []
        for mentoralt in Mentoral.tjai(mentor):
            lista += list(Hf.objects.filter(user=mentoralt))
        return lista

    def utolso_megoldasa(a_hf):
        return Mo.objects.filter(hf=a_hf).order_by('ido').last()

    def et_mar_mentoralta(a_hf, a_user) -> bool:
        for biralat in Biralat.objects.filter(mo=a_hf.utolso_megoldasa()):
            if biralat.mentor == a_user:
                return True
        return False

    def megoldasai_es_biralatai(a_hf):
        result = []
        for a_mo in Mo.objects.filter(hf=a_hf).order_by('ido'):
            result.append({'megoldas': True, 'tartalom':a_mo})
            result += [{'megoldas': False, 'tartalom':b} for b in Biralat.objects.filter(mo=a_mo).order_by('ido')]
        return result

    def allapot(a_hf) -> str:
        """
        lehetséges értékei:
        - NINCS_REPO: a mentorált még nem változtatta meg a default repo linket azaz a https://github.com/ -ot.
        - NINCS_MO: a mentoráltnak már van repo-ja, de még nem nyújtott be megoldást rá.
        - NINCS_BIRALAT: a mentoráltnak már van repoja, van utolsó megoldása, amire viszont még nem kapott bírálatot.
        - VAN_NEGATIV_BIRALAT: a mentoráltnak már van repoja, van utolsó megoldása és ennek van bírálata is: ezek közt viszont van egy negatív.
        - MINDEN_BIRALAT_POZITIV: a mentoráltnak már van repoja, van utolsó megoldása és ennek minden bírálata pozitív.
        """
        if a_hf.url == "https://github.com/":
            return "NINCS_REPO"
        az_utolso_megoldas = a_hf.utolso_megoldasa()
        if az_utolso_megoldas == None:
            return "NINCS_MO"
        az_utolso_megoldas_biralatai = Biralat.objects.filter(mo=az_utolso_megoldas)
        if not az_utolso_megoldas_biralatai.exists():
            return "NINCS_BIRALAT"
        for biralat in az_utolso_megoldas_biralatai:
            if biralat.itelet!="Elfogadva":
                return "VAN_NEGATIV_BIRALAT"
        return "MINDEN_BIRALAT_POZITIV"

    def mibol_mennyi(a_user):
        szotar = {}
        for oldal in ['hf', 'mo']:
            for allapot in ['uj', 'javit', 'biral', 'kesz']:
                szotar[oldal+allapot] = 0


        for a_hf in Hf.objects.all():
            # print(f'ez most a hf: {a_hf}')
            if a_hf.user == a_user:
                oldal = "hf"
            elif Mentoral.ja(a_user, a_hf.user): 
                oldal = "mo"
            else:
                continue

            allapot = allapotszotar[a_hf.allapot()]
            szotar[oldal + allapot] += 1
            
        return szotar
            

    def lista_to_template(hflista, a_user):

        result = []
        for a_hf in hflista:
            a_hf_allapota = a_hf.allapot()
            elem = {
                'tulajdonosa': a_hf.tulajdonosa,
                'cim': a_hf.kituzes.feladat.nev,
                'url': a_hf.url,
                'ha_mentoralt_akkor_neki_fontos': not a_user == a_hf.user or a_hf.allapot not in ["MINDEN_BIRALAT_POZITIV"],
                'ha_mentor_akkor_neki_fontos': not Mentoral.ja(a_user, a_hf.user) or (a_hf.allapot not in ["NINCS_REPO", "NINCS_MO"] and not a_hf.et_mar_mentoralta(a_user)),
                'allapot': a_hf_allapota,
                'allapotszuro': allapotszotar[a_hf_allapota],
                'hatarido': a_hf.hatarido,
                'mar_mentoralta': a_hf.et_mar_mentoralta(a_user),
                'hatralevoido': (a_hf.hatarido-datetime.now(timezone.utc)).days,
                'temai': list(map(lambda t: t.temakor.nev, Tartozik.objects.filter(feladat=a_hf.kituzes.feladat))),
                'id':a_hf.id,
                'kituzes': a_hf.kituzes,
            }
            print(elem['kituzes'])
            result.append(elem)
        return result

    
class Mo(models.Model):
    hf = models.ForeignKey(Hf, on_delete=models.CASCADE)
    szoveg = models.CharField(max_length=255)
    ido = models.DateTimeField(auto_now = True)
    
    class Meta:
        verbose_name = 'Megoldás'
        verbose_name_plural = 'Megoldások'

    def __str__(self):
        return f'{self.hf.user}, {self.hf.kituzes.feladat} ({self.ido}):{self.hf.url})'

    def nak_van_elutasito_biralata(a_mo) -> bool:
        biralatok = Biralat.objects.filter(mo=a_mo)
        for a_biralat in biralatok:
            if a_biralat.szoveg!="Elfogadva":
                return True
        return False

    def nak_van_pozitiv_biralata_es_csak_az_van(a_mo) -> bool:
        biralatok = Biralat.objects.filter(mo=a_mo)
        if not biralatok.exists():
            return False
        for a_biralat in biralatok:
            if a_biralat.szoveg!="Elfogadva":
                return False        
        return True
    
    def nak_nincs_biralata_vagy_van_negativ_biralata(a_mo) -> bool:
        a_biralatok = Biralat.objects.filter(mo=a_mo)
        if not a_biralatok.exists():
            return True
        for a_biralat in a_biralatok:
            if a_biralat.itelet != "Elfogadva":
                return True
        return False
            
        



class Biralat(models.Model):
    mo = models.ForeignKey(Mo, on_delete=models.CASCADE)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    szoveg = models.TextField()
    itelet = models.CharField(max_length=100)
    kozossegi_szolgalati_percek = models.IntegerField()
    ido = models.DateTimeField(auto_now = True)
    
    class Meta:
        verbose_name = 'Bírálat'
        verbose_name_plural = 'Bírálatok'

    def __str__(self):
        return f'{self.mentor}, {self.itelet}: {self.szoveg if len(self.szoveg)<=100 else (self.szoveg[:100]+"...")} ({self.mo.hf.kituzes.feladat}, {self.mo.hf.user})'
        
    @property
    def kozossegi_szolgalati_orak(self) -> str:
        return f"{ self.kozossegi_szolgalati_percek // 60 }:{ self.kozossegi_szolgalati_percek % 60 }" if self.kozossegi_szolgalati_percek > -1 else ""

    def van_elutasito(a_mo: Mo) -> bool:
        for biralat in Biralat.objects.filter(mo=a_mo):
            if biralat.itelet != "Elfogadva":
                return True
        return False

