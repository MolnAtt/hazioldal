# Közreműködés

Olvasd végig ezt az útmutatót, ha meg szeretnéd tudni, hogy hogyan tudsz hozzájárulni érdemben a házioldal fejlesztéséhez.

## Git guide
Ne commitolj az upstream repo-ba! Forkold a [MolnAtt/hazioldal](/github.com/MolnAtt/hazioldal) repo-t és az ott eszközölt commitok létrejöttével nyiss egy pull requestet.

> [!WARNING]
> Ha nem egy kisebb frontend hibát javítasz, akkor mindenképpen teszteld le egy devszerveren, hogy működik-e a módosításod! Ha lehet, akkor csatolj screenshotokat a pull request leírásában vagy alatta kommentben.

## Kisebb frontend hibák
Amennyiben kisebb frontend problémát veszel észre, amelyet úgy gondolod, hogy ki tudsz javítani, akkor akár már online a GitHub editorral vagy egy GitHub Codespace-el kijavíthatod.

Ilyen hiba lehet:
- CSS rule hiba
- Kifejezetten apró hibák templatekben, amelyek legfeljebb typo-k, de leginkább csak megjelenő feliratok, mert minden template tag a backenden babrál, így tesztelni kellene.

## Devszerver Windowson - Quickstart
Főleg backend teszteléséhez

Így tudsz **Windowson** közreműködni. Egyéb rendszereken a virtualenv és a Python könyvtárak eltérő módon működhetnek. Vedd figyelembe azt, hogy ezen útmutató egy úgynevezett "devszervert" segít létrehozni, amelyet létrehozza a házioldal másolatát a saját gépeden és nem feltétlenül érhető el más eszközről, publikálása ezen útmutató alaján nem javasolt.
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
> [!TIP]
> **Ellenőrizd**, hogy Windows rendszeren a `psycopg2-binary` könyvtár települ-e a requirements.txt szerint, mivel Linuxon `psycopg2` az ugyanazon rendeltetésű könyvtár neve.
```shell
pip install -r requirements.txt --no-input --ignore-installed
```
5. Nevezd át a `example_local_settings.py` fájlt `local_settings.py`-ra
6. Generálj egy secret key-t (opcionális, de ajánlott)
```shell
django-admin shell
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```
7. Másold be a `local_settings.py` megfelelő változójába (opcionális, de ajánlott)
```py
SECRET_KEY = '<te kulcsod>'
```
8. Nevezd át a `example.sqlite3` fájlt `db.sqlite3`-ra (opcionális, de ajánlott)

Ezen lépés kihagyása jelentősen megnövelné a beállítás időtartamát, mivel manuálisan kellene minden egyes modellt beállítani. 

Ezzel a telepítéssel már dolgozhatsz az alábbi témákban:
- Frontend: APP applikációban
- APP applikáció : models, views, urls, stb.

> [!WARNING]
> Ezek nem fognak működni, további beállítást igényelnek:
> - app_naplo futtatása(postgres adatbázis *szükséges*)
> - E-mailek küldése (local_settings-ben be kell állítani)

#### Example database (sqlite)
A repository tartalmaz egy példaadatbázist, amelyet példaadatokkal töltöttünk fel. Ez egy kis adatbázis, nem arra szolgál, hogy nagymennyiségű adatot hogyan dolgoz fel a rendszer, kizárólag a működéshez legszükségesebb adatokat tartalmazza.

1 mentor, 1 mentorált
1 adminisztrátor-tanár
4 mintafeladat
2 témakörben

| Felhasználó jellege   | Felhasználó        | Jelszó      |
|-----------------------|--------------------|-------------|
| Adminisztrátor-tanár  | admin              | admin       |
| Mentor                | nagymentor_pistike | pistike123  |
| Mentorált             | kisdiak_moriczka   | moriczka123 |

## Haladó közreműködés

>[!WARNING]
> Jelenleg nem létezik fejlesztőink által kibocsátott útmutató erre a kifejezett projekthez, ami megmondaná például, hogy hogyan lehet teljeskörű devszervert beállítani.
>
> Amennyiben mégis szeretnéd ezeket a funkciókat igénybe venni, a legjobb tanácsunk az, hogy találd fel magad és próbáld meg beállítani a PostgreSQL adatbázis magad.
>
> Ha pedig rendkívül jófejnek érzed magad, készítsd el ezen útmutató folytatását :D
