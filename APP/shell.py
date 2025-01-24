# vannak scriptek, amiket gyakran írok be a shellbe. Ezek szerepelnek itt, hogy később újrahasználhatók legyenek. 

from APP.models import *

szotar = {}
for b in Biralat.objects.all():
    if b.kozossegi_szolgalati_percek in szotar.keys():
        szotar[b.kozossegi_szolgalati_percek].append(b)
    else: 
        szotar[b.kozossegi_szolgalati_percek] = [b]

szotar = dict(sorted(szotar.items()))
standard_idok = [-1, 0, 1, 2]+list(range(5, 100, 5))

for ido in szotar.keys():
    print(f'{ido} perc: {len(szotar[ido])} db')
    if ido not in standard_idok:
        print(', '.join([str(b.id) for b in szotar[ido]]))

for ido in szotar.keys():
    if ido not in standard_idok:
        i = 0
        while standard_idok[i] <= ido:
            i+=1
        if i+1 < len(standard_idok):
            print(f'{ido} -> {standard_idok[i+1]}')
            for b in szotar[ido]:
                b.kozossegi_szolgalati_percek = standard_idok[i+1]
                b.save()



# BACKUP
from APP.models import *
modellek_backup()

# bírálatok és közösségi szolgálatok adatvesztés utáni helyreállítás

from APP.models import *
from datetime import datetime, timedelta
for bi in Biralat.objects.exclude(mentor__username='mattila').filter(ido__lte=datetime(2025, 1, 22)):
    bi.ido = bi.mo.ido + timedelta(minutes=1)
    bi.save()

