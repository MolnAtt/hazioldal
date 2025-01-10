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



