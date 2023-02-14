from django.db import models
from django.contrib.auth.models import User, Group
from APP.models import Tanit
from django.contrib.postgres.fields import ArrayField

# class Tanit(models.Model):
#     tanar = models.ForeignKey(User, on_delete=models.CASCADE)
#     csoport = models.ForeignKey(Group, on_delete=models.CASCADE)
    
#     class Meta:
#         verbose_name = 'Tanár-Csoport reláció'
#         verbose_name_plural = 'Tanár-Csoport relációk'

#     def __str__(self):
#         return f'{self.tanar} --- {self.csoport}'


class Dolgozat(models.Model):

    nev = models.CharField(max_length=255)
    slug = models.SlugField()
    osztaly = models.ForeignKey(Group, on_delete=models.CASCADE)
    tanar = models.ForeignKey(User, on_delete=models.CASCADE)
    tanulok = ArrayField(models.IntegerField(default=1))
    feladatok = ArrayField(models.CharField(max_length=255))
    feladatmaximumok = ArrayField(models.FloatField(default=0))
    matrix = ArrayField(ArrayField(models.FloatField(default=-1)))
    datum = models.DateTimeField()
    suly = models.FloatField()
    kettes_ponthatar = models.FloatField()
    harmas_ponthatar = models.FloatField()
    negyes_ponthatar = models.FloatField()
    otos_ponthatar = models.FloatField()
    duplaotos_ponthatar = models.FloatField()
    egyketted_hatar = models.FloatField()
    ketharmad_hatar = models.FloatField()
    haromnegyed_hatar = models.FloatField()
    negyotod_hatar = models.FloatField()


    class Meta:
        verbose_name = "Dolgozat"
        verbose_name_plural = "Dolgozatok"

    def __str__(self):
        return f"{self.nev} ({self.osztaly})"

    @property
    def name(self):
        return f"{self.slug}"
    
    @property
    def tanuloi(self):
        return list(map(lambda az_id: User.objects.get(id=az_id), self.tanulok))
    
    def meretei(a_dolgozat):
        return len(a_dolgozat.matrix), len(a_dolgozat.matrix[0]) if len(a_dolgozat.matrix) != 0 else (0,0)
    
    
    def IQR(kvartilis:tuple):
        return kvartilis[3]-kvartilis[1]
    
    def jegyertek(jegy:str) -> float:
        if jegy == '1/2':
            return 1.5
        if jegy == '2/3':
            return 2.5
        if jegy == '3/4':
            return 3.5
        if jegy == '4/5':
            return 4.5
        if jegy == '5*':
            return 5
        return int(jegy)
    
    def statisztika(a_dolgozat):
        pontok = [ pont for pont in (a_dolgozat.osszpontszam(User.objects.get(id = userid)) for userid in a_dolgozat.tanulok) if 0 < pont ]
        N = len(pontok)
        pontok.sort()
        
        maxpontszam = sum(a_dolgozat.feladatmaximumok)
        szazalekok = [ osszpontszam/maxpontszam for osszpontszam in pontok]
        jegyek = [ Dolgozat.jegyertek(a_dolgozat.osztalyzat(szazalek)) for szazalek in szazalekok]
        
        
        atlag_pont = Dolgozat.atlag(pontok)
        atlag_szazalek = Dolgozat.atlag(szazalekok)
        atlag_jegy = Dolgozat.atlag(jegyek)
        
        kvartilis_szazalek = Dolgozat.kvartilisek(szazalekok, N)
        
        return {
            'atlag': {
                'pont': atlag_pont,
                'szazalek': atlag_szazalek,
                'jegy': atlag_jegy,
                },
            'kvartilis': {
                'pont': Dolgozat.kvartilisek(pontok, N),
                'szazalek': kvartilis_szazalek,
                'jegy': Dolgozat.kvartilisek(jegyek, N),
                },
            'modusz': {
                'pont': Dolgozat.modusz(pontok),
                'szazalek': Dolgozat.modusz(szazalekok), # ennek mondjuk nem sok értelme van
                'jegy': Dolgozat.modusz(jegyek),
                },
            'atlagos_abszolut_elteres': {
                'pont': sum([abs(atlag_pont-pont) for pont in pontok]) / N,
                'szazalek': sum([abs(atlag_szazalek-szazalek) for szazalek in szazalekok]) / N,
                'jegy': sum([abs(atlag_jegy-jegy) for jegy in jegyek]) / N,
                },
            'szorasnegyzet': {
                'pont': sum([(atlag_pont-pont)**2 for pont in pontok]) / N,
                'szazalek': sum([(atlag_szazalek-szazalek)**2 for szazalek in szazalekok]) / N,
                'jegy': sum([(atlag_jegy-jegy)**2 for jegy in jegyek]) / N,
                },
            'IQR_grafikon': [szazalek for szazalek in szazalekok if kvartilis_szazalek[1] <= szazalek and szazalek <= kvartilis_szazalek[3]],
        }
    
    def rmedian(rlista:list)->int:
        N = len(rlista)
        if N == 0:
            return -1
        return (rlista[N//2 - 1] + rlista[N//2]) / 2 if N%2==0 else rlista[N//2 - 1]
    
    def kvartilisek(rlista:list, N:int) -> tuple:
        if N==0:
            return (0,0,0,0,0)
        
        return (
            rlista[0], 
            Dolgozat.rmedian(rlista[:N//2]),
            Dolgozat.rmedian(rlista),
            Dolgozat.rmedian(rlista[N//2+(0 if N % 2 == 0 else 1):]),
            rlista[-1], 
            )
    
    def modusz(rlista:list) -> list:
        szotar = {}
        for e in rlista:
            if e in szotar.keys():
                szotar[e] +=1
            else:
                szotar[e] = 1
              
        maxdb = 0  
        for k in szotar.keys():
            if maxdb < szotar[k]:
                maxdb = szotar[k]
        
        return [ k for k in szotar.keys() if szotar[k] == maxdb ]
    
    def outliers(ertekek, kvartilis, epsilon:float) -> list:
        return [e for e in ertekek if e < kvartilis[1]-epsilon] + [e for e in ertekek if e > kvartilis[3]+epsilon]
        
    
    def feladatstatisztika(a_dolgozat, userindex, feladatindex:int) -> dict:        
        ertekek = [ pont for pont in (a_dolgozat.matrix[ti][feladatindex] for ti,_ in enumerate(a_dolgozat.tanulok)) if 0 < pont]
        ertekek.sort()
        
        N = len(ertekek)
        
        kvartilis = Dolgozat.kvartilisek(ertekek, N)
        iqr = kvartilis[3] - kvartilis[1]
        
        return {
            'pont': a_dolgozat.matrix[userindex][feladatindex],
            'maxpont': a_dolgozat.feladatmaximumok[feladatindex],
            'atlag' : Dolgozat.atlag(ertekek),
            'modusz' : Dolgozat.modusz(ertekek),
            'kvartilis': kvartilis,
            'boxplot-min': max(kvartilis[0], kvartilis[1]-1.5*iqr),
            'boxplot-max': min(kvartilis[4], kvartilis[3]+1.5*iqr),
            'outliers': Dolgozat.outliers(ertekek, kvartilis, 1.5*iqr),
            'extreme_outliers': Dolgozat.outliers(ertekek, kvartilis, 3*iqr),
        }
        
    def ponthatarszotar(a_dolgozat)->dict:
        return {
            "1/2": a_dolgozat.kettes_ponthatar - a_dolgozat.egyketted_hatar,
            "2": a_dolgozat.kettes_ponthatar,
            "2/3": a_dolgozat.harmas_ponthatar - a_dolgozat.ketharmad_hatar,
            "3": a_dolgozat.harmas_ponthatar,
            "3/4": a_dolgozat.negyes_ponthatar - a_dolgozat.haromnegyed_hatar,
            "4": a_dolgozat.negyes_ponthatar,
            "4/5": a_dolgozat.otos_ponthatar - a_dolgozat.negyotod_hatar,
            "5": a_dolgozat.otos_ponthatar,
            "5*": a_dolgozat.duplaotos_ponthatar,
        }

    def statisztika_feladatonkent(a_dolgozat, userid:int) -> dict:
        feladatonkent = {}
        for i, feladat in enumerate(a_dolgozat.feladatok):
            feladatonkent[feladat] = a_dolgozat.feladatstatisztika(userid, i)
        return feladatonkent

    def json(a_dolgozat, a_user:User) -> dict:
        
        return {
            'nev': a_dolgozat.nev,
            'slug': a_dolgozat.slug,
            'csoport': a_dolgozat.osztaly.name,
            'tanar': a_dolgozat.tanar.username,
            'datum': a_dolgozat.datum,
            'suly' : a_dolgozat.suly,
            'ertekeles': a_dolgozat.ertekeles(a_user),
            'ponthatar': a_dolgozat.ponthatarszotar(),
            'feladatonkent': a_dolgozat.statisztika_feladatonkent(a_dolgozat.tanulok.index(a_user.id)),
            'statisztika': a_dolgozat.statisztika(),
        }
    
    def szotar(self):
        result = {}
        N = len(self.matrix)
        if N==0:
            return result
        
        M = len(self.matrix[0])
        for i,t in enumerate(self.tanuloi):
            result[t.username] = {}
            for j,f in enumerate(self.feladatok):
                if i<N and j<M:
                    result[t.username][f] = self.matrix[i][j]
        return result

    def ertekeloszotar(a_dolgozat):
        result = {}
        for tanuloid in a_dolgozat.tanulok:
            tanulo = User.objects.filter(id=tanuloid).first()
            if tanulo!=None:
                result[tanulo] = a_dolgozat.ertekeles(tanulo)
            else:
                print(f'valami baj van, nem találok egy tanulót: {tanuloid}')
        return result

    def nullmatrix(sorhalmaz, oszlophalmaz):
        return [[-1 for elem in oszlophalmaz] for sor in sorhalmaz]

    def matrix_inicializalasa(a_dolgozat):
        a_dolgozat.matrix = Dolgozat.nullmatrix(a_dolgozat.tanulok, a_dolgozat.feladatok)
        a_dolgozat.save()
    
    @property
    def tsv(self):
        tsv = ""
        for sor in self.matrix:
            for elem in sor[0:-1]:
                tsv += str(elem) + "\t"            
            tsv += str(sor[-1]) + "\n"
        return tsv.strip()

    def importfromtsv(self, tsv):
        self.matrix = [[ int(elem.strip()) for elem in sor.split('\t')] for sor in tsv.split('\n')]
        print(self.matrix)
        self.save()

    def median(lista):
        l = sorted([x for x in lista if 0<=x])
        N = len(l)
        if N == 0:
            return -1
        return l[N//2] if N % 2 == 1 else (l[N//2 - 1] + l[N//2])/2
    
    def maximum(lista):
        l = [x for x in lista if 0<=x]
        if len(l) == 0:
            return -1
        return max(l) 

    def minimum(lista):
        l = [x for x in lista if 0<=x]
        if len(l) == 0:
            return -1
        return min(l)

    def atlag(lista):
        l = [x for x in lista if 0<=x]
        if len(l) == 0:
            return -1
        return round(sum(l)/len(l),2)

    def osszesites(a_dolgozat, fuggveny):
        m = a_dolgozat.matrix
        N = len(m)
        if N == 0:
            raise Exception('Üres a dolgozatmátrix!')
        M = len(m[0])
        return [ fuggveny([m[i][j] for i in range(N)]) for j in range(M) ]


    def osszpontszam(a_dolgozat, a_tanulo:User) -> float:
        return sum( [ feladatpont for feladatpont in a_dolgozat.matrix[a_dolgozat.tanulok.index(a_tanulo.id)]])
            
    def osztalyzat(a_dolgozat, szazalek) -> str:
        szazalek*=100
        if a_dolgozat.duplaotos_ponthatar <= szazalek:
            return "5*"
        if a_dolgozat.otos_ponthatar < szazalek:
            return "5"
        if a_dolgozat.otos_ponthatar - a_dolgozat.negyotod_hatar < szazalek:
            return "4/5"
        if a_dolgozat.negyes_ponthatar < szazalek:
            return "4"
        if a_dolgozat.negyes_ponthatar - a_dolgozat.haromnegyed_hatar < szazalek:
            return "3/4"
        if a_dolgozat.harmas_ponthatar < szazalek:
            return "3"
        if a_dolgozat.harmas_ponthatar - a_dolgozat.ketharmad_hatar < szazalek:
            return "2/3"
        if a_dolgozat.kettes_ponthatar < szazalek:
            return "2"
        if a_dolgozat.kettes_ponthatar - a_dolgozat.egyketted_hatar < szazalek:
            return "1/2"
        if 0 <= szazalek:
            return "1"
        return "-"
        
    
    def ertekeles(a_dolgozat, tanulo):
        osszpontszam = a_dolgozat.osszpontszam(tanulo)
        if  osszpontszam < 0:
            return {
                'pont': '-',
                'szazalek': '-',
                'jegy': '-',
                }
        
        szazalek = float(osszpontszam)/sum(a_dolgozat.feladatmaximumok)
        return {
            'pont': osszpontszam,
            'szazalek': szazalek,
            'jegy': a_dolgozat.osztalyzat(szazalek),
            }
            
        