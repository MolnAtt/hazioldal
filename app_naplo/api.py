from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from datetime import datetime
from APP.seged import dictzip, ez_a_tanev
from app_naplo.models import Dolgozat, Lezaras
from django.http import JsonResponse
from APP.views import aktualis_tanev_eleje
from django.utils import timezone


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
def write_pont(request, group_name, dolgozat_slug):
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
    # tanuloid = int(request.data['tanuloid'])
    j_feladat = int(request.data['j_feladat'])
    az_ertek_str = request.data['ertek']
    az_ertek = -1
    try:
        az_ertek = float(az_ertek_str.replace(",","."))
    except:
        return Response(f"ez az érték nem tizedestört.")
    
    # a_tanulo = User.objects.filter(id=tanuloid).first()
    # if a_tanulo==None:
    #     return Response(f"{tanuloid} id-jű tanuló nem létezik, ezért nem tudom regisztrálni a pontot")
    
    if i_tanulo<0 or len(a_dolgozat.tanulok)<=i_tanulo:
        return Response(f"{i_tanulo} sorszámú tanuló sajnos nincs a névsorban, ezért nem tudom regisztrálni a pontot")
    
    a_dolgozat.matrix[i_tanulo][j_feladat] = az_ertek
    a_dolgozat.save()
    
    return Response(f"m[{i_tanulo}][{j_feladat}] = {az_ertek} értékadás végrehajtva")

@api_view(['POST'])
def write_suly(request, group_name, dolgozat_slug):
    if not request.user.groups.filter(name='adminisztrator').exists():
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    a_group = Group.objects.filter(name=group_name).first()
    if a_group == None:
        return Response(f'Ilyen csoport nincs: {group_name}', status=status.HTTP_404_NOT_FOUND)
    
    a_dolgozat = Dolgozat.objects.filter(slug=dolgozat_slug, osztaly=a_group).first()
    if a_dolgozat == None:
        return Response(f'Ilyen dolgozat nincs: {dolgozat_slug}', status=status.HTTP_404_NOT_FOUND)
    
    if 'sorszam' not in request.data.keys():
        return Response(f'Nincs "sorszam" kulcs a databan', status=status.HTTP_404_NOT_FOUND)

    try:
        sorszam = int(request.data['sorszam'])
    except:
        return Response(f"ez az érték ({ request.data['sorszam'] }) nem alakítható egész számmá.", status=status.HTTP_403_FORBIDDEN)

    az_ertek_str = request.data['ertek']
    az_ertek = -1
    try:
        az_ertek = float(az_ertek_str.replace(",","."))
    except:
        return Response(f"ez az érték nem tizedestört.", status=status.HTTP_403_FORBIDDEN)
    
    if sorszam<0 or len(a_dolgozat.tanulok)<=sorszam:
        return Response(f"{sorszam} sorszámú tanuló sajnos nincs a névsorban, ezért nem tudom regisztrálni a súlyvektor változtatását", status=status.HTTP_404_NOT_FOUND)
    
    if len(a_dolgozat.sulyvektor)<=sorszam:
        return Response(f"Rossz a súlyvektor hossza, mert nincs benne {sorszam}. elem", status=status.HTTP_404_NOT_FOUND)

    a_dolgozat.sulyvektor[sorszam] = az_ertek
    a_dolgozat.save()
    
    return Response(f"sulyvektor[{sorszam}] = {az_ertek} értékadás végrehajtva")

@api_view(['POST'])
def write_ponthatar(request,group_name,dolgozat_slug):
    if not request.user.groups.filter(name='adminisztrator').exists():
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    a_group = Group.objects.filter(name=group_name).first()
    if a_group == None:
        return Response(f'Ilyen csoport nincs: {group_name}', status=status.HTTP_404_NOT_FOUND)
    
    a_dolgozat = Dolgozat.objects.filter(slug=dolgozat_slug, osztaly=a_group).first()
    if a_dolgozat == None:
        return Response(f'Ilyen dolgozat nincs: {dolgozat_slug}', status=status.HTTP_404_NOT_FOUND)
    

    a_dolgozat.kettes_ponthatar = float(request.data['2'])
    a_dolgozat.harmas_ponthatar = float(request.data['3'])
    a_dolgozat.negyes_ponthatar = float(request.data['4'])
    a_dolgozat.otos_ponthatar = float(request.data['5'])
    a_dolgozat.egyketted_hatar = float(request.data['12'])
    a_dolgozat.ketharmad_hatar = float(request.data['23'])
    a_dolgozat.haromnegyed_hatar = float(request.data['34'])
    a_dolgozat.negyotod_hatar = float(request.data['45'])
    a_dolgozat.duplaotos_ponthatar = float(request.data['55'])
    a_dolgozat.suly = float(request.data['dolgozatsuly'])
    
    a_dolgozat.save()
    
    return Response(f"{a_dolgozat} ponthatárai sikeresen módosítva")
    


    

@api_view(['POST'])
def write_lezaras_jegy(request,group_name):
    if 'jegy' not in request.data.keys():
        return Response(f'nincs jegy key a databan', status=status.HTTP_404_NOT_FOUND)
    jegy_str = request.data['jegy']
    try:
        jegy = int(jegy_str)
    except:
        return (None, Response(f'a jegy ({ jegy_str }) nem alakítható számmá', status=status.HTTP_403_FORBIDDEN))

    
    lezaras, a_group, a_tanulo, response = Lezaras.get(request, group_name)

    if response != None:
        return response

    if lezaras == None:
        Lezaras.objects.create(csoport=a_group, tanulo=a_tanulo, jegy=jegy)
        return Response(f"{a_tanulo.last_name} {a_tanulo.first_name} lezárva {esre_asra(jegy)} (új lezárás jött így létre)", status=status.HTTP_200_OK)
    regi_jegy = lezaras.jegy
    lezaras.jegy = jegy
    lezaras.save()
    return Response(f"{a_tanulo.last_name} {a_tanulo.first_name} lezárva {esre_asra(jegy)} (jegy átírva {esrol_asrol(regi_jegy)} {esre_asra(jegy)})", status=status.HTTP_200_OK)

@api_view(['POST'])
def write_lezaras_szoveg(request,group_name):

    if 'szoveg' not in request.data.keys():
        return Response(f'nincs szoveg key a databan', status=status.HTTP_404_NOT_FOUND)
    
    lezaras, a_group, a_tanulo, response = Lezaras.get(request, group_name)

    if response != None:
        return response

    if lezaras == None:
        lezaras = Lezaras.objects.create(csoport=a_group, tanulo=a_tanulo, szoveg=request.data['szoveg'])
        return Response(f"{a_tanulo.last_name} {a_tanulo.first_name} még nincs lezárva (0-ás jegy), de kapott szöveges értékelést: {lezaras.szoveg}", status=status.HTTP_200_OK)
    regi_szoveg = lezaras.szoveg
    lezaras.szoveg = request.data['szoveg']
    lezaras.save()
    return Response(f"{a_tanulo.last_name} {a_tanulo.first_name} lezárásánál a szöveges értékelés megváltozott:  {regi_szoveg}  ----> {lezaras.szoveg})", status=status.HTTP_200_OK)

def esre_asra(i:int) -> str:
    if i == 5:
        return '5-ösre'
    if i == 3:
        return '3-asra'
    return f'{i}-esre'

def esrol_asrol(i:int) -> str:
    if i == 5:
        return '5-ösről'
    if i == 3:
        return '3-asról'
    return f'{i}-esről'
    
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
        matrix = Dolgozat.nullmatrix(a_tanulok, a_feladatok),
        sulyvektor = Dolgozat.egysegvektor(a_tanulok),
    )
    
    return Response({
        'uzenet': 'A dolgozat rendben elkészült.',
        'ev': ez_a_tanev(),
        }, status=status.HTTP_201_CREATED)

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
def read_dolgozat(request, group_name:str, dolgozat_slug:str, tanulo_id:int):

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
    
    a_user = User.objects.filter(id=tanulo_id).first()
    if a_user == None:
        return Response(f'Nincs is "{tanulo_id}" id-vel tanuló.', 
            status=status.HTTP_404_NOT_FOUND)
    
    # return Response(f'{a_dolgozat},{a_user},{a_group}', status=status.HTTP_200_OK)
    
    return Response(a_dolgozat.json(a_user), status=status.HTTP_200_OK)



    