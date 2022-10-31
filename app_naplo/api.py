from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from datetime import datetime
from APP.seged import dictzip

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
def write_pont(request):
    if not request.user.groups.filter(name='adminisztrator').exists():
        return Response(status=status.HTTP_403_FORBIDDEN)
    print(request.data)
    tanuloid = int(request.data['tanuloid'])
    feladatid = int(request.data['feladatid'])
    az_ertek_str = request.data['ertek']
    torles_kell = az_ertek_str == '-'
    az_ertek = -1
    try:
        if not torles_kell:
            az_ertek = int(az_ertek_str)
    except:
        return Response(f"ez az érték nem szám és nem kötőjel.")
    
    a_tanulo = User.objects.filter(id=tanuloid).first()
    if a_tanulo == None:
        return Response(f"{tanuloid} id-vel rendelkező tanuló sajnos nincs, ezért nem tudom regisztrálni a pontot")
    
    a_feladat = Feladat.objects.filter(id=feladatid).first()
    if a_feladat == None:
        return Response(f"{feladatid} id-vel rendelkező feladat sajnos nincs, ezért nem tudom regisztrálni a pontot")

    a_pont = Pont.objects.filter(user=a_tanulo, feladat=a_feladat).first()
    if a_pont == None:
        if not torles_kell:
            Pont.objects.create(user=a_tanulo, feladat=a_feladat, ertek=int(az_ertek))
            return Response(f"{a_tanulo} {a_feladat} feladatra kapott {az_ertek} pontja létre lett hozva")
        else: 
            return Response(f"{a_tanulo} {a_feladat} feladata nem létezik, szóval nem tudom törölni")
    else:
        if not torles_kell:
            a_pont.ertek = az_ertek
            a_pont.save()
            return Response(f"{a_tanulo} {a_feladat} feladatra kapott pontszáma {az_ertek} értékre lett módosítva")
        else: 
            a_pont.delete()
            return Response(f"{a_tanulo} {a_feladat} feladatra kapott pontszáma mindenestül törlésre került.")
            
