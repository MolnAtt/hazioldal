from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from datetime import datetime
from APP.seged import dictzip
from app_naplo.models import Dolgozat

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
        az_ertek = int(az_ertek_str)
    except:
        return Response(f"ez az érték nem szám.")
    
    if i_tanulo<0 or len(a_dolgozat.tanulok)<=i_tanulo:
        return Response(f"{i_tanulo} sorszámú tanuló sajnos nincs a névsorban, ezért nem tudom regisztrálni a pontot")
    
    a_dolgozat.matrix[i_tanulo][j_feladat] = az_ertek
    a_dolgozat.save()
    
    return Response(f"m[{i_tanulo}][{j_feladat}] = {az_ertek} értékadás végrehajtva")
    
