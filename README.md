# hazioldal
Új, git alapú házioldal. 
## Contributing
### Hogyan tudok közreműködni? - Quickstart
Így tudsz Windowson közreműködni. Egyéb rendszereken a virtualenv és a python könyvtárak eltérő módon működhetnek.
1. Klónozd a repo-t
2. A repo mappájában készíts egy Python Virtual Enviromentet(`venv` vagy `nodeenv`)
```shell
python -m venv env
```
3. Használd innentől a környezetet
```shell
env\Scripts\activate.bat
```
4. Futtasd le a következő parancsot, a könyvtárak telepítéséhez, megfelelő ellenőrzés után
**Ellenőrizd**, hogy Windows rendszeren a `psycopg2-binary` könyvtár ki van e kommentelve a requirements fájlban, Linuxon `psycopg2`.
```shell
pip install -r requirements.txt
```
5. Nevezd át a `example_local_settings.py` fájlt `local_settings.py`-ra
6. Generálj egy secret keyt
```shell
django-admin shell
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```
7. Másold be a `local_settings.py` megfelelő változójába
```py
SECRET_KEY = '<te kulcsod>'
```
8. Nevezd át a `example.sqlite3` fájlt `db.sqlite3`-ra

Ezzel a telepítéssel már dolgozhatsz az alábbi témákban:
- Frontend: APP applikációban
- APP applikáció : models, views, urls, stb.

Ezek nem fognak működni, további beállítást igényelnek:
- app_naplo futtatása(postgres adatbázis *szükséges*)
- E-mailek küldése (local_settings-ben be kell állítani)

### Example database (sqlite)
1 mentor, 1 mentorált
1 adminisztrátor-tanár
4 mintafeladat
2 témakörben

| Felhasználó jellege | Mentorált        | Mentor             | Adminisztrátor-tanár |
|---------------------|------------------|--------------------|----------------------|
| username            | kisdiak_moriczka | nagymentor_pistike | admin                |
| password            | moriczka123      | pistike123         | admin                |