# from inspect import classify_class_attrs
# from msilib.schema import Class
from pyexpat import model
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime, timezone
from django.utils import timezone as tz
from django.utils import dateformat
from APP.seged import ez_a_tanev, evnyito, kov_evnyito

def ki(s,v):
    print(f'{s} \t= \t{v}')

""" Állapotok lehetséges értékei:"""

NINCS_REPO = "NINCS_REPO"
# a mentorált még nem változtatta meg a default repo linket azaz a https://github.com/ -ot.
NINCS_MO = "NINCS_MO"
# a mentoráltnak már van repo-ja, de még nem nyújtott be megoldást rá.
NINCS_BIRALAT = "NINCS_BIRALAT"
# a mentoráltnak már van repoja, van utolsó megoldása, amire viszont még nem kapott bírálatot.
VAN_NEGATIV_BIRALAT = "VAN_NEGATIV_BIRALAT"
# a mentoráltnak már van repoja, van utolsó megoldása és ennek van bírálata is: ezek közt viszont van egy negatív.
MINDEN_BIRALAT_POZITIV = "MINDEN_BIRALAT_POZITIV"
# a mentoráltnak már van repoja, van utolsó megoldása és ennek minden bírálata pozitív.

ALLAPOTOK = (
    (NINCS_REPO, NINCS_REPO),
    (NINCS_MO, NINCS_MO),
    (NINCS_BIRALAT, NINCS_BIRALAT),
    (VAN_NEGATIV_BIRALAT, VAN_NEGATIV_BIRALAT),
    (MINDEN_BIRALAT_POZITIV , MINDEN_BIRALAT_POZITIV),
)

HALADEK_ALLAPOTOK = (
    ("hianyzas", "hianyzas"), 
    ("mentoralas", "mentoralas"),
    ("egyeb", "egyeb"),
)

HALADEK_BIRALATOK = (
    ("elfogadott", "elfogadott"),
    ("elutasitott", "elutasitott"),
    ("fuggo", "fuggo"),
)

allapotszotar = {
    NINCS_REPO : 'uj',
    NINCS_MO : 'uj',
    NINCS_BIRALAT : 'biral',
    VAN_NEGATIV_BIRALAT: 'uj',
    MINDEN_BIRALAT_POZITIV : 'kesz',
}


""" Kérelmek lehetséges típusai: """

BETEGSEG = "Betegség"
# A diák beteg és ezért haladékot kér a házi feladata elkészítéséhez.
MELTANYOSSAG = "Méltányosság"
# A diák valamilyen egyéb ok miatt szeretne haladékot kérni a házi feladatával kapcsolatban.

KERELMEK = (
    (BETEGSEG, BETEGSEG),
    (MELTANYOSSAG, MELTANYOSSAG),
)


class HaziCsoport(models.Model):

    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    ev = models.IntegerField()
    szekcio = models.CharField(max_length=8)
    tagozat = models.CharField(max_length=8)
    egyeb = models.CharField(max_length=64)


    class Meta:
        verbose_name = "Csoport"
        verbose_name_plural = "Csoportok"

    @property
    def osztaly(self):
        return f'{self.ev}.{self.szekcio}'
    
    def __str__(self):
        return f'{self.osztaly} {self.tagozat}'
    
    def tagjai(self):
        return (user.git for user in self.group.user_set.all())

    def tagja(self, user:User):
        return user in self.group.user_set
    
    def hazifeladatai(self):
        result = []
        tagok = set(self.tagjai())
        for hf in Hf.objects.all():
            if hf.user.git in tagok:
                result.append(hf)
        return result


class Git(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    count_of_nincs_repo = models.IntegerField(default=0)
    count_of_nincs_mo = models.IntegerField(default=0)
    count_of_nincs_biralat = models.IntegerField(default=0)
    count_of_van_negativ_biralat = models.IntegerField(default=0)
    count_of_minden_biralat_pozitiv = models.IntegerField(default=0)
    count_of_mentoraltnal_nincs_repo = models.IntegerField(default=0)
    count_of_mentoraltnal_nincs_mo = models.IntegerField(default=0)
    count_of_mentoraltnal_nincs_biralat = models.IntegerField(default=0)
    count_of_mentoraltnal_van_negativ_biralat = models.IntegerField(default=0)
    count_of_mentoraltnal_minden_biralat_pozitiv = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Git-profil'
        verbose_name_plural = 'Git-profilok'

    def __str__(self):
        return f'[{self.count_of_nincs_repo} {self.count_of_nincs_mo} {self.count_of_nincs_biralat} {self.count_of_van_negativ_biralat} {self.count_of_minden_biralat_pozitiv} | {self.count_of_mentoraltnal_nincs_repo} {self.count_of_mentoraltnal_nincs_mo} {self.count_of_mentoraltnal_nincs_biralat} {self.count_of_mentoraltnal_van_negativ_biralat} {self.count_of_mentoraltnal_minden_biralat_pozitiv}] {self.user.last_name} {self.user.first_name} ({self.username})'
    
    def tanar(self):
        return 'tanar' in [ gn[0] for gn in self.user.groups.values_list('name')]
    
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
    
    def hazifeladatai(self):
        return None
    
    def update_hf_counts(self) -> dict:
        hfek = Hf.objects.filter(user=self.user)

        counts = {}
        for allapot in allapotszotar.keys():
            counts[allapot] = 0
            
        for hf in hfek:
            # hf.update_allapot()            
            counts[hf.allapot]+=1
        
        self.count_of_nincs_repo = counts[NINCS_REPO]
        self.count_of_nincs_mo = counts[NINCS_MO]
        self.count_of_nincs_biralat = counts[NINCS_BIRALAT]
        self.count_of_van_negativ_biralat = counts[VAN_NEGATIV_BIRALAT]
        self.count_of_minden_biralat_pozitiv = counts[MINDEN_BIRALAT_POZITIV]
        
        self.save()
        
        return counts
    
    def update_mentor_counts(self) -> dict:
        mentoraltjai = [ a_user.mentoree.git for a_user in Mentoral.objects.filter(mentor=self.user)]
        
        self.count_of_mentoraltnal_nincs_repo = sum([mentoralt.count_of_nincs_repo for mentoralt in mentoraltjai])
        self.count_of_mentoraltnal_nincs_mo = sum([mentoralt.count_of_nincs_mo for mentoralt in mentoraltjai])
        self.count_of_mentoraltnal_nincs_biralat = sum([mentoralt.count_of_nincs_biralat for mentoralt in mentoraltjai])
        self.count_of_mentoraltnal_van_negativ_biralat = sum([mentoralt.count_of_van_negativ_biralat for mentoralt in mentoraltjai])
        self.count_of_mentoraltnal_minden_biralat_pozitiv = sum([mentoralt.count_of_minden_biralat_pozitiv for mentoralt in mentoraltjai])

        self.save()


    def update_counts_mentoralt_miatt(self):
        self.update_hf_counts()
        for mentor in Mentoral.oi(self.user):
            mentor.git.update_mentor_counts()

    def update_counts_mentor_miatt(self):
        for mentoralt in Mentoral.tjai(self.user):
            mentoralt.git.update_hf_counts()
        self.update_mentor_counts()

    
    def mibol_mennyi(gu):
        szotar = {}

        szotar['hfuj'] = gu.count_of_nincs_repo + gu.count_of_nincs_mo + gu.count_of_van_negativ_biralat
        szotar['hfbiral'] = gu.count_of_nincs_biralat
        szotar['hfkesz'] = gu.count_of_minden_biralat_pozitiv
        szotar['mouj'] = gu.count_of_mentoraltnal_nincs_repo + gu.count_of_mentoraltnal_nincs_mo + gu.count_of_mentoraltnal_van_negativ_biralat
        szotar['mobiral'] = gu.count_of_mentoraltnal_nincs_biralat
        szotar['mokesz'] = gu.count_of_mentoraltnal_minden_biralat_pozitiv
        
        
        
        # for allapot in ['uj', 'biral', 'kesz']:
        #     szotar['mo' + allapot] = 0
                
        


        # for a_hf in Hf.objects.all():
        #     # print(f'ez most a hf: {a_hf}')
        #     if a_hf.user == gu.user:
        #         oldal = "hf"
        #     elif Mentoral.ja(gu.user, a_hf.user): 
        #         oldal = "mo"
        #     else:
        #         continue

        #     allapot = allapotszotar[a_hf.allapot]
        #     szotar[oldal + allapot] += 1
            
        return szotar
        
        


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
        return f'{self.mentor} ---> {self.mentoree}'

    def ja(a_mentor: User, a_mentoralt: User) -> bool:
        return Mentoral.objects.filter(mentor=a_mentor, mentoree=a_mentoralt).exists()

    def tjai(a_mentor: User):
        return [m.mentoree for m in Mentoral.objects.filter(mentor=a_mentor)]

    def oi(a_mentoralt: User):
        return [m.mentor for m in Mentoral.objects.filter(mentoree=a_mentoralt)]





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
    temai = models.ManyToManyField(Temakor)
    
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
    
    def migracio(self):
        self.feladat.temai.add(self.temakor)


class Kituzes(models.Model):
    tanar = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True)
    feladat = models.ForeignKey(Feladat, on_delete=models.CASCADE)
    ido = models.DateTimeField(auto_now = True)
    hatarido = models.DateTimeField(null=True, blank=True)
    
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
    allapot = models.CharField(max_length=50, choices=ALLAPOTOK, default=NINCS_REPO)
    
    class Meta:
        verbose_name = 'Házi feladat'
        verbose_name_plural = 'Házi feladatok'

    def __str__(self):
        return f'{self.kituzes.feladat} ({self.user}, {self.hatarido}{", mentoralando" if self.mentoralando else ""})'

    @property
    def tulajdonosa(a_hf):
        return f"{a_hf.user.last_name} {a_hf.user.first_name}"

    def elso_megoldas(a_hf):
        return a_hf.mo_set.order_by('ido').first()

    def elso_megoldas_ideje(a_hf):
        elsomo = a_hf.elso_megoldas()
        if elsomo==None:
            return None
        return elsomo.ido

    def elso_megoldas_ideje_str_hn(a_hf):
        dt = a_hf.elso_megoldas_ideje()
        if dt==None:
            return ''
        return dateformat.format(dt, "M. d.")

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
    
    def idei(a_hf) -> bool:
        ezatanev = ez_a_tanev()
        d = a_hf.hatarido.date()
        return evnyito(ezatanev).date() <= d and d <= kov_evnyito(ezatanev).date()

    def kockaview(a_userek, a_csoport_kituzesei):
        userek_sorai = []
        for a_user in a_userek:
            a_user_hazifeladatai = []
            for a_kituzes in a_csoport_kituzesei:
                a_hf = Hf.objects.filter(user=a_user, kituzes=a_kituzes).first()
                a_user_hazifeladatai.append(a_hf if a_hf != None else {'na':'valami'} )
                
            userek_sorai.append({
                'user': a_user,
                'hazifeladatai': a_user_hazifeladatai,
                'mentorai': [mentor for mentor in Mentoral.oi(a_user) if not mentor.git.tanar()],
                })
            
        return userek_sorai


    def megoldasai_es_biralatai(a_hf):
        result = []
        for a_mo in Mo.objects.filter(hf=a_hf).order_by('ido'):
            result.append({'megoldas': True, 'tartalom':a_mo})
            result += [{'megoldas': False, 'tartalom':b} for b in Biralat.objects.filter(mo=a_mo).order_by('ido')]
        return result

    def update_allapot(a_hf) -> str:
        """
        lehetséges értékei:
        - NINCS_REPO: a mentorált még nem változtatta meg a default repo linket azaz a https://github.com/ -ot.
        - NINCS_MO: a mentoráltnak már van repo-ja, de még nem nyújtott be megoldást rá.
        - NINCS_BIRALAT: a mentoráltnak már van repoja, van utolsó megoldása, amire viszont még nem kapott bírálatot.
        - VAN_NEGATIV_BIRALAT: a mentoráltnak már van repoja, van utolsó megoldása és ennek van bírálata is: ezek közt viszont van egy negatív.
        - MINDEN_BIRALAT_POZITIV: a mentoráltnak már van repoja, van utolsó megoldása és ennek minden bírálata pozitív.
        """
        if a_hf.url == "https://github.com/":
            a_hf.allapot = NINCS_REPO
        else:
            az_utolso_megoldas = a_hf.utolso_megoldasa()
            if az_utolso_megoldas == None:
                a_hf.allapot = NINCS_MO
            else:
                az_utolso_megoldas_biralatai = Biralat.objects.filter(mo=az_utolso_megoldas)
                if az_utolso_megoldas_biralatai.first() == None:
                    a_hf.allapot = NINCS_BIRALAT
                elif a_hf.van_negativ_biralat(az_utolso_megoldas_biralatai):
                    a_hf.allapot = VAN_NEGATIV_BIRALAT
                else:
                    a_hf.allapot = MINDEN_BIRALAT_POZITIV
        a_hf.save()
        return a_hf.allapot
    
    def van_negativ_biralat(a_hf, az_utolso_megoldas_biralatai) -> bool:
        for biralat in az_utolso_megoldas_biralatai:
            if biralat.itelet!="Elfogadva":
                return True
        return False

    def elso_ertekelheto_megoldasa(a_hf):
        ''' keressük az első megoldást, ami határidőn belül van ÉS nincs értékelhetetlennek mondott bírálata '''
        for a_mo in a_hf.mo_set.all():
            if a_mo.ido.date() <= a_hf.hatarido.date() and a_mo.nem_ertekelhetetlen():
                return a_mo
        return None               
        
    
    def amnesztia_lezar(a_hf, a_datetime, az_admin):
        
        melyik = 3
        az_allapot = a_hf.allapot
        if a_hf.allapot == NINCS_REPO:
            a_hf.url+="amnesztia"
            a_hf.save()
            az_allapot = NINCS_MO
            melyik = 0

        a_mo = None
        if az_allapot == NINCS_MO:
            a_mo = Mo.objects.create(hf=a_hf, szoveg=f"amnesztia {a_datetime}", ido = a_datetime)
            az_allapot = NINCS_BIRALAT
            if melyik < 1:
                melyik = 1
        else:
            a_mo = a_hf.utolso_megoldasa()

        if az_allapot == NINCS_BIRALAT:
            a_biralat = Biralat.objects.create(
                mo = a_mo, 
                mentor = az_admin, 
                szoveg = f"amnesztia {a_datetime}",
                itelet = "Elfogadva",
                kozossegi_szolgalati_percek = 0,
                ido = a_datetime
                )
            if melyik < 2:
                melyik = 2
        a_hf.update_allapot()
        return melyik
        

    def hatarideje_lejart(a_hf):
        return a_hf.hatarido < tz.now()
    
    def nek_nincs_ertekelheto_megoldasa(a_hf):
        '''
        - nincs leadva megoldás
            vagy
        - van leadva megoldás, de arra van legalább egy olyan bírálat, amely szerint az értékelhetetlen.
        '''
        megoldasok = Mo.objects.filter(hf=a_hf)
        if not megoldasok.exists():
            return True
        
        for mo in megoldasok:
            if mo.nem_ertekelhetetlen():
                return False
        return True
        
        

    # def mibol_mennyi(a_user):
    #     szotar = {}
    #     for oldal in ['hf', 'mo']:
    #         for allapot in ['uj', 'javit', 'biral', 'kesz']:
    #             szotar[oldal+allapot] = 0


    #     for a_hf in Hf.objects.all():
    #         # print(f'ez most a hf: {a_hf}')
    #         if a_hf.user == a_user:
    #             oldal = "hf"
    #         elif Mentoral.ja(a_user, a_hf.user): 
    #             oldal = "mo"
    #         else:
    #             continue

    #         allapot = allapotszotar[a_hf.allapot]
    #         szotar[oldal + allapot] += 1
            
    #     return szotar
            

    def lista_to_template(hflista, a_user):
        return [{
                'tulajdonosa': a_hf.user,
                'githubfelhasznaloneve': a_hf.user.git.username,
                'mentorai': [mentor for mentor in Mentoral.oi(a_hf.user) if not mentor.git.tanar()],
                'cim': a_hf.kituzes.feladat.nev,
                'url': a_hf.url,
                'ha_mentoralt_akkor_neki_fontos': not a_user == a_hf.user or a_hf.allapot not in [MINDEN_BIRALAT_POZITIV],
                'ha_mentor_akkor_neki_fontos': not Mentoral.ja(a_user, a_hf.user) or (a_hf.allapot not in [NINCS_REPO, NINCS_MO] and not a_hf.et_mar_mentoralta(a_user)),
                'allapot': a_hf.allapot,
                'allapotszuro': allapotszotar[a_hf.allapot],
                'hatarido': a_hf.hatarido,
                'mar_mentoralta': a_hf.et_mar_mentoralta(a_user),
                'hatralevoido': (a_hf.hatarido-datetime.now(timezone.utc)).days,
                'temai': a_hf.kituzes.feladat.temai,
                'id':a_hf.id,
                'kituzes': a_hf.kituzes,
            } for a_hf in hflista]


    
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
            
    def nem_ertekelhetetlen(a_mo):
        '''Nem értékelhetetlen, ha nincs egy értékelhetetlen minősítés sem.'''
        for bi in a_mo.biralat_set.all():
            if bi.itelet == "Értékelhetetlen":
                return False
        return True
        



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

class Haladek_kerelem(models.Model):

    datum = models.DateTimeField(auto_now=True)
    tipus = models.CharField(max_length=64, choices=HALADEK_ALLAPOTOK, default="egyeb")
    targy = models.CharField(max_length=128)
    body = models.TextField()
    url = models.URLField(max_length=256, blank=True, null=True)
    hf = models.ForeignKey(Hf, on_delete=models.CASCADE)
    nap = models.IntegerField()
    elbiralva = models.CharField(max_length=64, choices=HALADEK_BIRALATOK, default="fuggo")

    class Meta:
        verbose_name = "Haladékkérelem"
        verbose_name_plural = "Haladékkérelmek"

    def __str__(self):
        return f'{self.hf.user}: {self.targy} ({self.tipus})'


class Egyes(models.Model):

    hf = models.ForeignKey(Hf, on_delete=models.CASCADE)
    datum = models.DateField(auto_now=True)
    kreta = models.BooleanField()

    class Meta:
        verbose_name = "Egyes"
        verbose_name_plural = "Egyesek"

    def __str__(self):
        return f'{"💀" if self.kreta else "💣" } {self.hf.user}: {self.datum}'

    def ek_kozul_az_utolso(a_hf:Hf):
        return Egyes.objects.filter(hf=a_hf).order_by('datum').last()

    def jarna_erte(a_hf:Hf):
        ''' 
        Egy házira egyes jár, ha
                - lejárt már a határidő
            és (ha van leadva megoldás, akkor arra létezik legalább egy olyan bírálat, amely szerint az értékelhetetlen)               
            és (ha kapott már rá egyest, akkor a legrégebbi ilyen egyes is öregebb 7 napnál).
                - nem kapott még rá egyest
                vagy
                - kapott már rá egyeset, de a legrégebbi kapott egyese is 7 napnál öregebb.
            
        - a legutóbbi egyes régebbi mint 7 nap
        '''

        if not a_hf.idei():
            return False
        
        ma = tz.now().date()
        hatarido_napja = a_hf.hatarido.date()

        elso_ertekelheto_mo = a_hf.elso_ertekelheto_megoldasa()
        if elso_ertekelheto_mo == None:
            return hatarido_napja < ma
        
        if hatarido_napja < elso_ertekelheto_mo.ido.date():

            utolsoegyes = Egyes.ek_kozul_az_utolso(a_hf)
            return (utolsoegyes == None) or (7 < (ma-utolsoegyes.datum).days)
        return False

    def beirasa(a_hf:Hf):
        siker = False
        if Egyes.jarna_erte(a_hf):
            e, siker =  Egyes.objects.get_or_create(hf = a_hf, kreta = False)
        return e if siker else None

    def ek_kiosztasa(csoport:HaziCsoport):
        most = tz.now()
        lista = []
        for hf in csoport.hazifeladatai():
            e = Egyes.beirasa(hf)
            if e!=None:
                lista.append(hf)
        return lista

    def ek_elozetes_felmerese(csoport:HaziCsoport):
        egyesek = [ f'{hf.user.last_name} {hf.user.first_name}: {hf.kituzes.feladat.nev} ({dateformat.format(hf.hatarido, "M. d.")} helyett {hf.elso_megoldas_ideje_str_hn()})' for hf in csoport.hazifeladatai() if Egyes.jarna_erte(hf)]
        return f'{len(egyesek)} db háziért járna egyes, mégpedig a következőkért:\n'+'\n'.join(egyesek)

    def kiosztas_visszajelzes(hazik):
        return "\n".join([f'{hf.user.last_name} {hf.user.first_name}: {hf.kituzes.feladat.nev} ({dateformat.format(hf.hatarido, "M. d.")})' for hf in hazik])

    def ei_egy_tanulonak(a_user:User, ettol:datetime, eddig:datetime):
        result = []
        for a_hf in Hf.objects.filter(user=a_user):
            result += list(Egyes.objects.filter(hf=a_hf, datum__range=(ettol, eddig)))
        return result
    
    
    def datetime(egyes):
        return datetime(egyes.datum.year, egyes.datum.month, egyes.datum.day)

    def date(egyes):
        return egyes.datum