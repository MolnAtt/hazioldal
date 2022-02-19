from rest_framework.response import Response
from rest_framework import status


def tagja(a_user, csoportnev):
    return a_user.groups.filter(name=csoportnev).exists()

# def admin(a_user):
#     return tagja(a_user, 'admin')

# def tanar(a_user):
#     return tagja(a_user, 'tanar')

def dictzip(szoveg):
    sorok = szoveg.strip().split('\n')
    mezonevek = sorok[0].strip().split('\t')+['sor']
    rekordok = list(map(lambda sor : dict(zip(mezonevek, sor.strip().split('\t')+[sor])), sorok[1:]))
    return rekordok

def get_or_error(klassz, az_id):
    a_cucc = klassz.objects.filter(id=az_id).first()
    if a_cucc == None:
        print(f"ezt az id-t kérték le a {klassz} classból, de ilyen nincs: {az_id}, ezért kap egy 404-et")
        return (None, Response(status=status.HTTP_404_NOT_FOUND))
    return (a_cucc, None)
