# from inspect import classify_class_attrs
# from msilib.schema import Class
from pyexpat import model
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime, timezone, timedelta
from django.utils import timezone as tz
from django.utils import dateformat
from APP.seged import ez_a_tanev, evnyito, kov_evnyito
from github import Github, Auth
import os

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



def datumkonyvtar(most:datetime):
    return f'{most.year}_{str(most.month).zfill(2)}_{str(most.day).zfill(2)}'

def backup(Model, tablanev, col_separator='\t', row_separator='\n', kiterjesztes='tsv'):
        mezonevsor = col_separator.join(Model.backup_mezonevek()) + row_separator
        konyvtar = 'backup' + '/' + datumkonyvtar(tz.now()) 
        if not os.path.exists(konyvtar):
            os.makedirs(konyvtar)
        open(konyvtar + '/' + tablanev + '.' + kiterjesztes, 'w', encoding='utf8').write(mezonevsor + row_separator.join(col_separator.join([str(elem) for elem in r.backup_elem()]) for r in Model.objects.all()))

def null_or_id(ob):
    return 'NULL' if ob==None else ob.id

def id_stringlista(mtmfield):
    return ','.join(str(t.id) for t in mtmfield.all())

class HaziCsoport(models.Model):

    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    ev = models.IntegerField()
    szekcio = models.CharField(max_length=8)
    tagozat = models.CharField(max_length=8)
    egyeb = models.CharField(max_length=64)

    def backup_mezonevek():
        return ['group_id', 'ev', 'szekcio', 'tagozat', 'egyeb']
    
    def backup_elem(r) -> list:
        return [r.group.id, r.ev, r.szekcio, r.tagozat, r.egyeb]

    def backup():
        backup(HaziCsoport, 'HaziCsoport')

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

    github_token = models.CharField(max_length=300, blank=True, null=True)
    commithistory = models.BooleanField(default=False)

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
    
    def backup_mezonevek():
        return ['user_id', 'username', 'email', 'platform', 'github_token', 'commithistory', 'count_of_nincs_repo', 'count_of_nincs_mo', 'count_of_nincs_biralat', 'count_of_van_negativ_biralat', 'count_of_minden_biralat_pozitiv', 'count_of_mentoraltnal_nincs_repo', 'count_of_mentoraltnal_nincs_mo', 'count_of_mentoraltnal_nincs_biralat', 'count_of_mentoraltnal_van_negativ_biralat', 'count_of_mentoraltnal_minden_biralat_pozitiv']
    
    def backup_elem(r) -> list:
        return [r.user.id, r.username, r.email, r.platform, r.github_token, r.commithistory, r.count_of_nincs_repo, r.count_of_nincs_mo, r.count_of_nincs_biralat, r.count_of_van_negativ_biralat, r.count_of_minden_biralat_pozitiv, r.count_of_mentoraltnal_nincs_repo, r.count_of_mentoraltnal_nincs_mo, r.count_of_mentoraltnal_nincs_biralat, r.count_of_mentoraltnal_van_negativ_biralat, r.count_of_mentoraltnal_minden_biralat_pozitiv]

    def backup():
        backup(Git, 'Git')

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
    
    def backup_mezonevek():
        return ['tanar_id', 'csoport_id']
    
    def backup_elem(r) -> list:
        return [r.tanar.id, r.csoport.id]

    def backup():
        backup(Tanit, 'Tanit')

    class Meta:
        verbose_name = 'Tanár-Csoport reláció'
        verbose_name_plural = 'Tanár-Csoport relációk'

    def __str__(self):
        return f'{self.tanar} --- {self.csoport}'


class Mentoral(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor')
    mentoree = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentoree')
    
    def backup_mezonevek():
        return ['mentor_id', 'mentoree_id']
    
    def backup_elem(r) -> list:
        return [r.mentor.id, r.mentoree.id]

    def backup():
        backup(Mentoral, 'Mentoral')


    class Meta:
        verbose_name = 'Mentorálás'
        verbose_name_plural = 'Mentorálás'

    def __str__(self):
        return f'{self.mentor} ---> {self.mentoree}'

    def e(a_mentor: User) -> bool:
        return None != Mentoral.objects.filter(mentor=a_mentor).first()

    def ja(a_mentor: User, a_mentoralt: User) -> bool:
        return Mentoral.objects.filter(mentor=a_mentor, mentoree=a_mentoralt).exists()

    def tjai(a_mentor: User):
        return [m.mentoree for m in Mentoral.objects.filter(mentor=a_mentor)]

    def oi(a_mentoralt: User):
        return [m.mentor for m in Mentoral.objects.filter(mentoree=a_mentoralt)]


class Temakor(models.Model):
    sorrend = models.CharField(max_length=255)
    nev = models.CharField(max_length=255)

    def backup_mezonevek():
        return ['sorrend', 'nev']
    
    def backup_elem(r) -> list:
        return [r.sorrend, r.nev]

    def backup():
        backup(Temakor, 'Temakor')


    class Meta:
        verbose_name = 'Témakör'
        verbose_name_plural = 'Témakörök'

    def __str__(self):
        return f'{self.nev} ({self.sorrend})'


class Feladat(models.Model):
    nev = models.CharField(max_length=255)
    url = models.URLField()
    temai = models.ManyToManyField(Temakor)
    
    def backup_mezonevek():
        return ['nev', 'url', 'temai_idset']
    
    def backup_elem(r) -> list:
        return [r.nev, r.url, id_stringlista(r.temai)]

    def backup():
        backup(Feladat, 'Feladat')


    class Meta:
        verbose_name = 'Feladat'
        verbose_name_plural = 'Feladat'

    def __str__(self):
        return f'{self.id}🆔{self.nev}'



class Kituzes(models.Model):
    tanar = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True)
    feladat = models.ForeignKey(Feladat, on_delete=models.CASCADE)
    ido = models.DateTimeField(auto_now_add = True)
    hatarido = models.DateTimeField(null=True, blank=True)
    
    def backup_mezonevek():
        return ['tanar_id', 'group', 'feladat', 'ido', 'hatarido']
    
    def backup_elem(r) -> list:
        return [r.tanar.id, r.group.id, r.feladat.id, r.ido]

    def backup():
        backup(Kituzes, 'Kituzes')


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

    def backup_mezonevek():
        return ['kituzes_id', 'user_id', 'hatarido', 'mentoralando', 'url', 'allapot']
    
    def backup_elem(r) -> list:
        return [r.kituzes.id, r.user.id, r.hatarido, r.mentoralando, r.url, r.allapot]

    def backup():
        backup(Hf, 'Hf')



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
    
    def new_mentorview(a_userek, a_csoport_kituzesei):
        feladatok_sorai = []
        for a_kituzes in a_csoport_kituzesei:
            a_kituzes_hazifeladatai = []
            for a_user in a_userek:
                a_hf = Hf.objects.filter(user=a_user, kituzes=a_kituzes).first()
                a_kituzes_hazifeladatai.append(a_hf if a_hf != None else {'na':'valami'} )
                
            feladatok_sorai.append({
                'kituzes': a_kituzes,
                'hazifeladatai': a_kituzes_hazifeladatai,
                })
        return feladatok_sorai
    
    # Heti nézet a házi feladatokhoz
    # Csak Mentoráltaknak működik - egy user kitűzéseit csekkolja csak
    def hetiview(a_user_kituzesei):
        hetibontas = {}
        a = ez_a_tanev()
        for a_hf in a_user_kituzesei:
            het = a_hf.hatarido.isocalendar()[1] # python 3.8-ban nincs még "week" property
            if het in hetibontas.keys():
                hetibontas[het].append(a_hf)
            else:
                hetibontas[het] = [a_hf]
        return dict(sorted(hetibontas.items(), key= lambda kv : kv[1][0].hatarido))

    def megoldasai_es_biralatai(a_hf, reponev=None):
        result = []
        for a_mo in Mo.objects.filter(hf=a_hf):
            result.append({'megoldas': 'megoldas', 'tartalom': a_mo, 'ido': tz.make_aware(a_mo.ido) if tz.is_naive(a_mo.ido) else a_mo.ido})
            result += [{'megoldas': 'biralat', 'tartalom': b, 'ido': tz.make_aware(b.ido) if tz.is_naive(b.ido) else a_mo.ido} for b in Biralat.objects.filter(mo=a_mo)]

        commits = []

        hiba = None
        if a_hf.user.git.commithistory and reponev:
            try:
                auth = Auth.Token(a_hf.user.git.github_token)
                g = Github(auth=auth)

                repo = g.get_repo(reponev.split("https://github.com/")[1].split(".git")[0])
                commitok = repo.get_commits()
                for commit in commitok:
                    commits.append(
                        {
                            "megoldas": "commit",
                            "ido": commit.commit.committer.date,
                            "message": commit.commit.message,
                            "url": commit.html_url,
                            }
                        )
            except Exception as e:
                hiba = e

        combined_result = result + commits
        
        # Events
        # nem működik valami a dátumokkal
        # events = []
        # events.append(
        #     {
        #     'megoldas': 'event',
        #     'event': 'kituzes',
        #     'ido': tz.make_aware(a_hf.kituzes.ido) if tz.is_naive(a_hf.kituzes.ido) else a_hf.kituzes.ido,
        #     'message': 'Feladat kitűzése',
        #     }
        # )

        # hatido = tz.make_aware(a_hf.hatarido) if tz.is_naive(a_hf.hatarido) else a_hf.hatarido

        # if a_hf.hatarido and tz.make_naive(hatido) <= datetime.now():
        #     events.append(
        #     {
        #         'megoldas': 'event',
        #         'event': 'hatarido',
        #         'ido': hatido,
        #         'message': 'Határidő lejárta',
        #     }
        #     )

        # combined_result += events

        combined_result.sort(key=lambda x: x['ido'])
        if hiba:
            combined_result.append(
                {
                    'hiba': hiba,
                    'megoldas': 'hiba',
                }
            )
        return combined_result

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
        ''' keressük az első megoldást, ami határidőn belül van 
            ÉS 
            nincs értékelhetetlennek mondott bírálata '''
        for a_mo in a_hf.mo_set.all():
            # if a_mo.ido.date() <= a_hf.hatarido.date() and a_mo.nem_ertekelhetetlen():
            if a_mo.nem_ertekelhetetlen():
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
        h = a_hf.hatarido
        hatarido = tz.make_aware(datetime(h.year, h.month, h.day) + timedelta(1))
        return tz.make_aware(hatarido) if tz.is_naive(hatarido) else (hatarido < tz.make_aware(tz.now())) if tz.is_naive(tz.now()) else tz.now(),
    
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
    ido = models.DateTimeField(auto_now_add = True)

    def backup_mezonevek():
        return ['hf_id', 'szoveg', 'ido']
    
    def backup_elem(r) -> list:
        return [r.hf.id, r.szoveg, r.ido]

    def backup():
        backup(Mo, 'Mo')


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
    ido = models.DateTimeField(auto_now_add = True)

    def backup_mezonevek():
        return ['mo_id', 'mentor_id', 'szoveg', 'itelet', 'kozossegi_szolgalati_percek', 'ido']
    
    def backup_elem(r) -> list:
        return [r.mo.id, r.mentor.id, r.szoveg, r.itelet, r.kozossegi_szolgalati_percek, r.ido]

    def backup():
        backup(Biralat, 'Biralat')



    class Meta:
        verbose_name = 'Bírálat'
        verbose_name_plural = 'Bírálatok'

    def __str__(self):
        return f'{self.mentor}, {self.itelet}: {self.szoveg if len(self.szoveg)<=100 else (self.szoveg[:100]+"...")} ({self.mo.hf.kituzes.feladat}, {self.mo.hf.user})'
        
    @property
    def kozossegi_szolgalati_orak(self) -> str:
        return f"{ self.kozossegi_szolgalati_percek // 60 }:{ self.kozossegi_szolgalati_percek % 60 }" if self.kozossegi_szolgalati_percek > -1 else ""

    def kozossegi_szolgalati_ido(self) -> tuple:
        return (self.kozossegi_szolgalati_percek // 60, self.kozossegi_szolgalati_percek % 60) if self.kozossegi_szolgalati_percek > -1 else (-1, -1)
    
    def kozossegi_szolgalati_ido_str(self) -> str:
        return f"{self.kozossegi_szolgalati_percek // 60}óra {self.kozossegi_szolgalati_percek % 60} perc" if self.kozossegi_szolgalati_percek % 60 > 0 else f"{self.kozossegi_szolgalati_percek // 60} óra" if self.kozossegi_szolgalati_percek > -1 else ""

    def van_elutasito(a_mo: Mo) -> bool:
        for biralat in Biralat.objects.filter(mo=a_mo):
            if biralat.itelet != "Elfogadva":
                return True
        return False


class Haladek_kerelem(models.Model):

    datum = models.DateTimeField(auto_now_add=True)
    tipus = models.CharField(max_length=64, choices=HALADEK_ALLAPOTOK, default="egyeb")
    targy = models.CharField(max_length=128)
    body = models.TextField()
    biralat = models.ForeignKey(Biralat, blank=True, null=True, on_delete=models.CASCADE)
    url = models.URLField(max_length=256, blank=True, null=True)
    hf = models.ForeignKey(Hf, on_delete=models.CASCADE)
    nap = models.IntegerField()
    elbiralva = models.CharField(max_length=64, choices=HALADEK_BIRALATOK, default="fuggo")
    valasz = models.TextField(blank=True, null=True)

    def backup_mezonevek():
        return ['datum', 'tipus', 'targy', 'body', 'biralat_id', 'url', 'hf_id', 'nap', 'elbiralva', 'valasz']    
    
    def backup_elem(r) -> list:
        return [r.datum, r.tipus, r.targy, r.body, null_or_id(r.biralat), r.url, null_or_id(r.hf), r.nap, r.elbiralva, r.valasz]

    def backup():
        backup(Haladek_kerelem, 'Haladek_kerelem')


    class Meta:
        verbose_name = "Haladékkérelem"
        verbose_name_plural = "Haladékkérelmek"
    
    def apporove(self, plusznapok=-1):
        # Azért kell ezt így megcsinálni, mert az argumentum megadásnál még nincs valamiért self(????)
        if plusznapok < 0:
            plusznapok = self.nap
        
        self.elbiralva = 'elfogadott'
        self.hf.hatarido += timedelta(days=plusznapok)
        self.hf.save()
        self.save()

        return True
    
    def deny(self):
        self.elbiralva = 'elutasitott'
        self.hf.hatarido = self.hf.kituzes.hatarido
        self.hf.save()
        self.save()

        return True
    
    def toPending(self):
        self.elbiralva = 'fuggo'
        self.hf.hatarido = self.hf.kituzes.hatarido
        self.hf.save()
        self.save()

        return True

    def emoji_state(self):
        if self.elbiralva == 'elfogadott':
            return '✔'
        if self.elbiralva == 'elutasitott':
            return '❌'
        return '⏳'

    def emoji_tipus(self):
        if self.tipus == 'hianyzas':
            return '🤒'
        if self.tipus == 'mentoralas':
            return '👷‍♂️'
        return '🕵️‍♂️'

    def __str__(self):
        return f'{self.emoji_state()}{self.nap}☀{self.emoji_tipus()}{self.hf.user.last_name} {self.hf.user.first_name}: {self.targy}'


class Egyes(models.Model):

    hf = models.ForeignKey(Hf, on_delete=models.CASCADE)
    datum = models.DateField(auto_now_add=True)
    kreta = models.BooleanField()
    suly = models.FloatField(default=1)

    def backup_mezonevek():
        return ['hf_id', 'datum', 'kreta', 'suly']    
    
    def backup_elem(r) -> list:
        return [r.hf.id, r.datum, r.kreta, r.suly]

    def backup():
        backup(Egyes, 'Egyes')


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

    def jarna_erte_indoklassal(a_hf:Hf):
        ''' 
        Ez egy script arra, hogy a leadott, elkésett, de a határidőkitolással(ápr 8) leadott házikat elfogadja utólag.

        from datetime import date
        from APP.models import *

        haladate = date(2024,4,8)
        for a_hf in Hf.objects.all():
            elso_mo = a_hf.elso_ertekelheto_megoldasa()
            if elso_mo != None and elso_mo.ido.date()>a_hf.hatarido.date() and elso_mo.ido.date()<= haladate:
                a_hf.hatarido = elso_mo.ido
                a_hf.save()
        '''

        eleje = f'Egyesvizsgálat: ' 
        vege = f' ({a_hf})'

        if not a_hf.idei():
            return False, eleje + 'nem idei' + vege
        
        ma = tz.now().date()
        hatarido_napja = a_hf.hatarido.date()
        print(f'ma: {ma}, hatarido_napja: {hatarido_napja}')

        elso_ertekelheto_mo = a_hf.elso_ertekelheto_megoldasa()
        if elso_ertekelheto_mo == None:
            if hatarido_napja < ma:
                return True, eleje + 'nincs értékelhető mo, határidő pedig lejárt' + vege
            else:
                return False, eleje + 'nincs értékelhető mo, de nem is járt le a határidő' + vege        

        if hatarido_napja < elso_ertekelheto_mo.ido.date():            
            utolsoegyes = Egyes.ek_kozul_az_utolso(a_hf)
            if (utolsoegyes == None) or (7 < (ma-utolsoegyes.datum).days):
                if utolsoegyes == None:
                    return True, eleje + 'elkésett az első értékelhető megoldással, és még nem kapott rá 1-est' + vege
                else: 
                    return True, eleje + 'van már egyese belőle, de az már több mint egy hetes' + vege
            else:
                return False, eleje + 'Kapott már egyest belőle, ami még elég friss (fiatalabb, mint egy hetes)' + vege
        return False, 'Van értékelhető megoldás, ami még a határidő napja előtt vagy aznap érkezett be.'

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
        # egyesek = [ f'{hf.user.last_name} {hf.user.first_name}: {hf.kituzes.feladat.nev} ({dateformat.format(hf.hatarido, "M. d.")} helyett {hf.elso_megoldas_ideje_str_hn()})' for hf in csoport.hazifeladatai() if Egyes.jarna_erte(hf)]
        egyesek = [ f'{hf.user.last_name} {hf.user.first_name}: {hf.kituzes.feladat.nev} ({dateformat.format(hf.hatarido, "M. d.")} helyett {hf.elso_megoldas_ideje_str_hn()}), indoklás: {Egyes.jarna_erte_indoklassal(hf)[1]}' for hf in csoport.hazifeladatai() if Egyes.jarna_erte(hf)]
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
    

class Kampany(models.Model):

    nev = models.CharField(max_length=255)
    graphviz = models.TextField()
    feladatai = models.ManyToManyField(Feladat, blank=True)
    svg = models.TextField()

    def backup_mezonevek():
        return ['nev', 'graphviz', 'feladatai', 'svg']    
    
    def backup_elem(r) -> list:
        return [r.nev, r.graphviz, id_stringlista(r.feladatai), r.svg]

    def backup():
        backup(Kampany, 'Kampany')


    class Meta:
        verbose_name = 'Kampány'
        verbose_name_plural = 'Kampányok'

    def __str__(self):
        return self.nev

    


MODELLEK = [HaziCsoport, Git, Tanit, Mentoral, Temakor, Feladat, Kituzes, Hf, Mo, Biralat, Haladek_kerelem, Egyes]

def modellek_backup():
    for m in MODELLEK:
        m.backup()

