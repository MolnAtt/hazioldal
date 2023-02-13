from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from datetime import datetime
from APP.seged import dictzip
from app_naplo.models import Dolgozat
from django.http import JsonResponse

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
def write_pont(request,group_name,dolgozat_slug):
    if not request.user.groups.filter(name='adminisztrator').exists():
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    a_group = Group.objects.filter(name=group_name).first()
    if a_group == None:
        return Response(f'Ilyen csoport nincs: {group_name}', status=status.HTTP_404_NOT_FOUND)
    
    a_dolgozat = Dolgozat.objects.filter(slug=dolgozat_slug, osztaly=a_group).first()
    if a_dolgozat == None:
        return Response(f'Ilyen dolgozat nincs: {dolgozat_slug}', status=status.HTTP_404_NOT_FOUND)
    
    # print(request.data)
    i_tanulo = int(request.data['i_tanulo'])
    j_feladat = int(request.data['j_feladat'])
    az_ertek_str = request.data['ertek']
    az_ertek = -1
    try:
        az_ertek = float(az_ertek_str.replace(",","."))
    except:
        return Response(f"ez az érték nem tizedestört.")
    
    if i_tanulo<0 or len(a_dolgozat.tanulok)<=i_tanulo:
        return Response(f"{i_tanulo} sorszámú tanuló sajnos nincs a névsorban, ezért nem tudom regisztrálni a pontot")
    
    a_dolgozat.matrix[i_tanulo][j_feladat] = az_ertek
    a_dolgozat.save()
    
    return Response(f"m[{i_tanulo}][{j_feladat}] = {az_ertek} értékadás végrehajtva")
    

def feladatcsv_feldolgozasa(csv):
    feladatok = []
    maxpontok = []
    for sor in csv.strip().split('\n'):
        sortomb = sor.split(';')
        feladatok.append(sortomb[0].strip())
        maxpontok.append(sortomb[1].strip())
    return (feladatok, maxpontok)
    
def html2datetime(datumstr):
    return array2datetime(datumstr.split('-'))

def array2datetime(datumsplit):
    return datetime(int(datumsplit[0]), int(datumsplit[1]), int(datumsplit[2]))
    
@api_view(['POST'])
def create_dolgozat(request):
    if not request.user.groups.filter(name='adminisztrator').exists():
        return Response('ehhez a funkcióhoz adminisztrátori jogosultság szükséges.', status=status.HTTP_403_FORBIDDEN)

    if Dolgozat.objects.filter(slug = request.data['dolgozat_slug']).exists():
        return Response('Ilyen sluggal már létezik dolgozat! Válassz másikat!', status=status.HTTP_403_FORBIDDEN)

    
    a_csoport = Group.objects.filter(name = request.data['csoport_nev']).first()
    if a_csoport == None:
        return Response('Ilyen csoport nincs!', status=status.HTTP_404_NOT_FOUND)
    
    a_feladatok, a_maxpontok = feladatcsv_feldolgozasa(request.data['feladatcsv'])
    
    a_tanulok = [tanulo.id for tanulo in User.objects.filter(groups__name=request.data['csoport_nev'])]
    Dolgozat.objects.create(
        nev = request.data['dolgozat_nev'],
        slug = request.data['dolgozat_slug'],
        osztaly = a_csoport,
        tanar = request.user,
        tanulok = a_tanulok,
        feladatok = a_feladatok,
        feladatmaximumok = a_maxpontok,
        suly = float(request.data['suly']),
        datum = html2datetime(request.data['datum']),
        kettes_ponthatar=float(request.data['ponthatar2']),
        harmas_ponthatar=float(request.data['ponthatar3']),
        negyes_ponthatar=float(request.data['ponthatar4']),
        otos_ponthatar=float(request.data['ponthatar5']),
        duplaotos_ponthatar=float(request.data['ponthatar55']),
        egyketted_hatar=float(request.data['ponthatar12']),
        ketharmad_hatar=float(request.data['ponthatar23']),
        haromnegyed_hatar=float(request.data['ponthatar34']),
        negyotod_hatar=float(request.data['ponthatar45']),
        matrix = Dolgozat.nullmatrix(a_tanulok, a_feladatok)
    )
    
    return Response('A dolgozat rendben elkészült.', status=status.HTTP_201_CREATED)

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


def has_a_group_in(user:User, group_name_list:list) -> bool:
    for group_name in group_name_list:
        if user.groups.filter(name=group_name).exists():
            return True
    return False

@api_view(['GET'])
def read_dolgozat(request,group_name,dolgozat_slug):
    a_user = request.user
    
    if not has_a_group_in(request.user, [group_name, 'adminisztrator', 'tanar']) :
        return Response(f'A "{dolgozat_slug}" dolgozathoz nem férsz hozzá, mert ezt egy olyan csoport ({group_name}) írta, amelynek te nem vagy tagja és nem vagy tanár vagy adminisztrátor sem', 
            status=status.HTTP_403_FORBIDDEN)

    a_group = Group.objects.filter(name=group_name).first()
    if a_group == None:
        return Response(f'Nincs is "{group_name}" nevű csoport.', 
            status=status.HTTP_404_NOT_FOUND)
    
    a_dolgozat = Dolgozat.objects.filter(slug=dolgozat_slug, osztaly=a_group).first()
    if a_dolgozat == None:
        return Response(f'Nincs "{dolgozat_slug}" névvel dolgozata a {group_name} csoportnak', 
            status=status.HTTP_404_NOT_FOUND)

    szotar = a_dolgozat.megtekintese(request.user)
    print(szotar)
    return Response(szotar, status=status.HTTP_200_OK)



    