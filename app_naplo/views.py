from tokenize import group
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .models import Dolgozat
from APP.models import Tanit
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound,  HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from APP.seged import tagja

@user_passes_test(lambda user : tagja(user, 'tanar'))
def index(request):
    template='app_naplo/valaszto.html'
    context={
        'cim': 'Napló',
        'linkek' : [
            { 'nev':  'Csoport regisztrációja', 'link':  'regisztracio'},
            { 'nev':  'Csoport kiválasztása', 'link':  'csoport'},
            ],
    }
    return render(request, template, context)


@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def csoportvalaszto(request):
    template = "app_naplo/valaszto.html"
    context = {
        'cim': 'Osztály kiválasztása',
        'linkek': list(map(lambda t: { 'nev':  t.csoport.name, 'link':  t.csoport.name}, Tanit.objects.filter(tanar = request.user))),
    }
    return render(request, template, context)


@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def dolgozatvalaszto(request, group_name):
    template = "app_naplo/valaszto.html"
    
    az_osztaly = Group.objects.filter(name=group_name).first()
    if az_osztaly==None:
        return HttpResponseNotFound(f"ilyen osztály nincs: {group_name}")

    context = {
        'cim': 'Dolgozat kiválasztása',
        'linkek': list(map(lambda t: { 'nev':  t.nev, 'link':  t.slug}, Dolgozat.objects.filter(osztaly = az_osztaly))),
    }
    return render(request, template, context)


@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def felhasznalok_regisztracioja(request):
    template = "app_naplo/userinput.html"
    context = {}
    return render(request, template, context)


@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def dolgozat(request, group_name, dolgozat_slug):
    template = "app_naplo/pontinput.html"
    a_group = Group.objects.filter(name=group_name).first()
    if a_group == None:
        return HttpResponseNotFound(f'Ilyen csoport nincs: {group_name}')
    a_dolgozat = Dolgozat.objects.filter(slug=dolgozat_slug, osztaly=a_group).first()
    if a_dolgozat == None:
        return HttpResponseNotFound(f'Ilyen dolgozat nincs: {dolgozat_slug}')
    
    context = {
        'a_dolgozat': a_dolgozat,
        'atlagok': a_dolgozat.osszesites(Dolgozat.atlag),
        'medianok': a_dolgozat.osszesites(Dolgozat.median),
        'minimumok': a_dolgozat.osszesites(min),
        'maximumok': a_dolgozat.osszesites(max),
        }
    return render(request, template, context)


def kivalaszt(klassz, kargok, megj='nem találtam meg'):
    result = klassz.objects.filter(**kargok).first()
    if result == None:
        raise Exception(megj)
    return result
    

@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def dolgozatmatrixeditor(request, group_name, dolgozat_slug):
    template = "app_naplo/dolgozattsvimport.html"
    
    a_group = Group.objects.filter(name=group_name).first()
    if a_group == None:
        return HttpResponseNotFound(f'Ilyen csoport nincs: {group_name}')
    
    a_dolgozat = Dolgozat.objects.filter(slug=dolgozat_slug, osztaly=a_group).first()
    if a_dolgozat == None:
        return HttpResponseNotFound(f'Ilyen dolgozat nincs: {dolgozat_slug}')
    
    if request.method=="POST":
        a_dolgozat.importfromtsv(request.POST['matrixtsv'])
    
    context = {
        'a_dolgozat': a_dolgozat,
    }
    return render(request, template, context)



@user_passes_test(lambda user : tagja(user, 'tanar'))
def dolgozat_download(request, group_name, dolgozat_slug):
    a_group = Group.objects.filter(name=group_name).first()
    if a_group == None:
        return HttpResponseNotFound(f'Ilyen csoport nincs: {group_name}')
    
    a_dolgozat = Dolgozat.objects.filter(slug=dolgozat_slug, osztaly=a_group).first()
    if a_dolgozat == None:
        return HttpResponseNotFound(f'Ilyen dolgozat nincs: {dolgozat_slug}')
    
    return HttpResponse(serializers.serialize("json", Dolgozat.objects.filter(id = a_dolgozat.id)))