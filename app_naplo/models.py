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
        
        
    def matrix_inicializalasa(a_dolgozat):
        a_dolgozat.matrix = [[-1 for elem in a_dolgozat.feladatok] for sor in a_dolgozat.tanulok]
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
        if  0 <= osszpontszam:
            maximum_elerheto_pontszam = sum(a_dolgozat.feladatmaximumok)
            szazalek = round(100*osszpontszam/maximum_elerheto_pontszam, 2)
            jegy = a_dolgozat.osztalyzat(szazalek)
            return {
                'pont': osszpontszam,
                'szazalek': szazalek,
                'jegy': jegy,
                }
        else:
            return {
                'pont': '-',
                'szazalek': '-',
                'jegy': '-',
                }
        