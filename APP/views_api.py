from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from APP.seged import dictzip, get_or_error, tagja

from .models import Git, Kituzes, Tartozik, Temakor, Feladat, Hf, Mo, Biralat, Mentoral
from django.contrib.auth.models import User, Group



####################################
## GIT API

@api_view(['POST'])
def create_git_for_all(request):
    if not request.user.is_authenticated or not tagja(request.user, 'adminisztrator'):
        return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(Git.letrehozasa_mindenkinek_ha_meg_nincs())

@api_view(['POST'])
def update_git(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    a_user = request.user
    a_user.git.username = request.data['username']
    a_user.git.save()
    return Response('git username sikeresen frissítve')


####################################
## HF API

def get_hf(request, hfid:int):
    if not request.user.is_authenticated:
        print(f"Előbb be kéne jelentkezni.")
        return (None, Response(status=status.HTTP_403_FORBIDDEN))
    a_hf = Hf.objects.filter(id=hfid).first()
    if a_hf == None:
        print(f"ezt a hf-et kérték le, de ilyen nincs: {hfid}, ezért kap egy 404-et")
        return (None, Response(status=status.HTTP_404_NOT_FOUND))
    if not (request.user == a_hf.user or Mentoral.ja(request.user, a_hf.user)):
        print(f"{request.user} sem nem mentoralt, sem nem mentor ebben a hfid={hfid} hf-ben, ezért kap egy 403 forbiddent")
        return (None, Response(status=status.HTTP_403_FORBIDDEN))
    return (a_hf, None)


@api_view(['GET'])
def read_hf(request, hfid:int):
    (a_hf, error) = get_hf(request, hfid)
    if error != None:
        return error
    return Response({
        'id': a_hf.id,
        'url': a_hf.url,
        })


@api_view(['POST'])
def update_hf(request, hfid):
    (a_hf, error) = get_hf(request, hfid)
    if error != None:
        return error
    if request.user != a_hf.user:
        print(f'a {request.user} felhasználónak nincs jogosultsága megváltoztatni a repo linkjét, erre csak {a_hf.user} felhasználónak van jogosultsága')
        return Response(status=status.HTTP_403_FORBIDDEN)    
    a_hf.url = request.data['url']
    a_hf.save()
    return Response(f'a {hfid} id-jű repo url-je módosítva erre: {a_hf.url}')


####################################
## MO API

@api_view(['POST'])
def create_mo(request, hfid):
    a_hf = Hf.objects.filter(id=hfid).first()
    if a_hf == None:
        print(f"nincs ilyen id-val repo: {hfid}.")
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.user != a_hf.user:
        print(f"ennek a usernek ({request.user}) nincs is jogosultsága megoldást feltölteni.")
        return Response(status=status.HTTP_403_FORBIDDEN)
    a_mo = Mo.objects.get_or_create(
        hf = a_hf, 
        szoveg = request.data['szoveg']
        )
    print("létrejött a mo" if a_mo[1] else "nem jött létre a mo mert már van ilyen ehhez a repohoz ilyen szoveggel")
    return Response({'moid':a_mo[0].id,'created':a_mo[1]})


####################################
## BIRALAT API

@api_view(['POST'])
def create_biralat(request, hfid):
    a_hf = Hf.objects.filter(id=hfid).first()
    if a_hf == None:
        print(f"nincs ilyen id-val repo: {hfid}.")
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not Mentoral.ja(request.user, a_hf.user):
        print(f"ennek a usernek ({request.user}) nincs is jogosultsága bírálatot feltölteni, mert nem mentora a repo ({a_hf}) tulajdonosának, aki {a_hf.hf.user}.")
        return Response(status=status.HTTP_403_FORBIDDEN)
    a_mo = a_hf.utolso_megoldasa()
    a_biralat = Biralat.objects.get_or_create(
        mo = a_mo, 
        mentor = request.user, 
        szoveg = request.data['szoveg'], 
        itelet = request.data['itelet'], 
        kozossegi_szolgalati_percek = -1,
        )
    print("létrejött a biralat" if a_biralat[1] else "nem jött létre a biralat mert már van ilyen ehhez a repohoz ilyen szoveggel")
    return Response({'biralatid':a_biralat[0].id,'created':a_biralat[1]})

@api_view(['DELETE'])
def delete_biralat(request, biralatid):
    a_biralat = Biralat.objects.filter(id=biralatid).first()
    if a_biralat == None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if a_biralat.mentor != request.user:
        print(f"ennek a usernek ({request.user}) nincs is jogosultsága ezt a bírálatot ({a_biralat}) törölni, mert ez nem az övé.")
        return Response(status=status.HTTP_403_FORBIDDEN)
    a_biralat.delete()
    return Response('ez bizony törölve lett')




#####################################
### USER API

@api_view(['POST'])
def create_users(request):
    if not request.user.groups.filter(name='adminisztrator').exists():
        return Response(status=status.HTTP_403_FORBIDDEN)

    rekordok = dictzip(request.data['szoveg'])

    db = 0
    for rekord in rekordok:
        a_user, user_created = get_or_create_user(rekord)
        if user_created:
            db += 1
        a_group, _ = Group.objects.get_or_create(name = rekord['group'])
        a_user.groups.add(a_group)
    uzenet = f'{db} db új user létrehozva a {len(rekordok)} db rekordból.'
    print(uzenet)
    return Response(uzenet)


def get_or_create_user(rekord):
    a_user = User.objects.filter(username=rekord['username']).first()
    if a_user != None:
        return (a_user, False)
    a_user = User.objects.create_user(  username = rekord['username'],
                                        email = rekord['email'],
                                        password = rekord['password'],
                                        last_name = rekord['last_name'],
                                        first_name = rekord['first_name'],
                                        )
    return (a_user, True)

@api_view(['POST'])
def update_activity(request):
    if not request.user.groups.filter(name='adminisztrator').exists():
        return Response(status=status.HTTP_403_FORBIDDEN)

    db = 0
    nem_adminisztratorok = [ u for u in User.objects.all() if not u.groups.filter(name='adminisztrator').exists()]
    for user in nem_adminisztratorok:
        if  user.is_active != request.data['active']:
            user.is_active = request.data['active']
            user.save()
            db += 1
    akt = "akt" if request.data['active'] else "passz"
    n = len(nem_adminisztratorok)
    uzenet = f'{db} db nem adminisztrátor user lett {akt}iválva a(z) {n} db ilyen userből.\n(Tehát {n-db} db user már korábban is {akt}ív volt.)'
    print(uzenet)
    return Response(uzenet)


#####################################
### MENTORAL API

@api_view(['POST'])
def create_mentoral(request):
    if not request.user.groups.filter(name='adminisztrator').exists():
        return Response(status=status.HTTP_403_FORBIDDEN)
    rekordok = dictzip(request.data['szoveg'])
    db = 0
    for rekord in rekordok:
        a_mentor = User.objects.get(username=rekord['mentor'])
        a_mentoree = User.objects.get(username=rekord['mentoree'])
        _, mentoralt_created = Mentoral.objects.get_or_create(mentor=a_mentor, mentoree=a_mentoree)
        if mentoralt_created:
            db += 1
    uzenet = f'{db} db új mentorkapcsolás létrehozva a {len(rekordok)} db rekordból.'
    print(uzenet)
    return Response(uzenet)

@api_view(['GET'])
def read_mentoral(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    a_user_mentorai = "\n".join([ user.git.username for user in Mentoral.oi(request.user)])
    print(f'a {request.user} lekérdezte a mentorait, akik: {a_user_mentorai}, {Mentoral.oi(request.user)}')
    return Response(a_user_mentorai)




#####################################
### FELADAT API

def get_temakor(request, temaid:int):
    a_temakor = Temakor.objects.filter(id=temaid).first()
    if a_temakor == None:
        print(f"ezt a témát kérték le, de ilyen nincs: {a_temakor}, ezért kap egy 404-et")
        return (None, Response(status=status.HTTP_404_NOT_FOUND))
    return (a_temakor, None)

@api_view(['GET'])
def read_tema_feladatai(request, temaid:int):
    (a_temakor, error) = get_temakor(request, temaid)
    if error != None:
        return error    
    return Response([ {'nev': f.feladat.nev, 'id': f.feladat.id} for f in Tartozik.objects.filter(temakor=a_temakor)])




#####################################
### KITUZES API

@api_view(['POST'])
def create_kituzes(request):
    if not request.user.groups.filter(name='tanar').exists():
        return Response(status=status.HTTP_403_FORBIDDEN)
            
    a_csoport, error = get_or_error(Group, request.data['csoportid'])
    if error!=None: 
        return error

    a_feladat, error = get_or_error(Feladat, request.data['feladatid'])
    if error!=None: 
        return error

    # a kitűzés létrehozása

    a_kituzes, created = Kituzes.objects.get_or_create(tanar=request.user, group=a_csoport, feladat=a_feladat)
    uzenet = ""
    if created:
        uzenet += f'új kitűzés lett létrehozva: {a_kituzes}'
    else:
        uzenet += f'ez a kitűzés már létezett korábban is: {a_kituzes}'
    

    # feladatok létrehozása
    
    db = 0
    datum = request.data['hatarido'].split('-')
    a_hatarido = datetime(int(datum[0]), int(datum[1]), int(datum[2]))
    for a_user in User.objects.filter(groups__name=a_csoport.name):
        _, created = Hf.objects.get_or_create(kituzes=a_kituzes, user=a_user, hatarido=a_hatarido)
        if created:
            db += 1

    uzenet += f" és a feladatok mindenki számára létre lettek hozva ({db} db)"
    return Response(uzenet)


