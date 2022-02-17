from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from APP.seged import dictzip

from .models import Hf, Mo, Biralat, Mentoral
from django.contrib.auth.models import User, Group


####################################
## HF API

def get_hf(request, hfid:int):
    a_hf = Hf.objects.filter(id=hfid).first()
    if a_hf == None:
        print(f"ezt a hf-et kérték le, de ilyen nincs: {hfid}, ezért kap egy 404-et")
        return (None, Response(status=status.HTTP_404_NOT_FOUND))
    if not (request.user == a_hf.user or Mentoral.ja(request.user, a_hf.user)):
        print(f"{request.user} sem nem mentoralt, sem nem mentor ebben a hfid={hfid} hf-ben, ezért kap egy 403 forbiddent")
        return (None, Response(status=status.HTTP_403_FORBIDDEN))
    return (a_hf, None)


@api_view(['GET'])
def hf_read(request, hfid:int):
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
    a_biralat = Biralat.objects.get(id=biralatid)
    if a_biralat.mentor != request.user:
        print(f"ennek a usernek ({request.user}) nincs is jogosultsága ezt a bírálatot ({a_biralat}) törölni, mert ez nem az övé.")
        return Response(status=status.HTTP_403_FORBIDDEN)
    a_biralat.delete()
    return Response('ez bizony törölve lett')




#####################################
### USER API

@api_view(['POST'])
def create_users(request):
    if not request.user.groups.filter(name='admin').exists():
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



#####################################
### MENTORAL API

@api_view(['POST'])
def create_mentoral(request):
    if not request.user.groups.filter(name='admin').exists():
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


