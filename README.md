# hazioldal
**Új, git alapú házioldal.**

## Leírás

Célja, hogy helyettesítse az előző, PHP alapú házioldalt, mely fenntarthatósági és dependencia problémák mellett, sok nagy fájlt kezelt, így a Házioldal ezen verziója már minden helyzetben igyekszik amilyen munkát csak lehet kiszervezni, de persze úgy, hogy nagy mértékben ne függjön tőle (kivéve Git).

## Motorháztető alatt
Django, mely egy appban kompatibilis sqlite adatbázisokkal, de a napló már PostgreSQL adatbázist igényel.

Frontenden plain HTML(Jinja - Django HTML), CSS és JS.

A beküldött szövegek Markdownként jelennek meg. A rendszer a létrehozott HTML-t
engedélyezési listával tisztítja; az eseménykezelők, egyéni stílusok, nem
biztonságos URL-ek és a nem engedélyezett HTML-elemek nem maradnak meg.

## Contributing - Hogyan tudok közreműködni?
[Kattints ide](CONTRIBUTING.md) a közreműködéssel kapcsolatos útmutatáshoz

## Bugok jelentése, feature requestek
Az egyszerűség kedvéért rendszerezetten lehet bugokat jelenteni, feature requesteket beköldeni GitHubon az **Issues** panelen.