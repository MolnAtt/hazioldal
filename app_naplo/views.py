from tokenize import group
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .models import Dolgozat
from APP.models import Tanit
from django.http import HttpResponseNotFound,  HttpResponseForbidden


def index(request):
    if not request.user.groups.filter(name='tanar').exists():
        return HttpResponseForbidden()
    template='app_naplo/valaszto.html'
    context={
        'cim': 'Napló',
        'linkek' : [
            { 'nev':  'Csoport regisztrációja', 'link':  'regisztracio'},
            { 'nev':  'Csoport kiválasztása', 'link':  'csoport'},
            ],
    }
    return render(request, template, context)


def csoportvalaszto(request):
    if not request.user.groups.filter(name='adminisztrator').exists():
        return HttpResponseForbidden()
    template = "app_naplo/valaszto.html"
    context = {
        'cim': 'Osztály kiválasztása',
        'linkek': list(map(lambda t: { 'nev':  t.csoport.name, 'link':  t.csoport.name}, Tanit.objects.filter(tanar = request.user))),
    }
    return render(request, template, context)


def dolgozatvalaszto(request, group_name):
    if not request.user.groups.filter(name='adminisztrator').exists():
        return HttpResponseForbidden()
    template = "app_naplo/valaszto.html"
    az_osztaly = Group.objects.filter(name=group_name).first()
    if az_osztaly==None:
        return HttpResponseNotFound()

    context = {
        'cim': 'Dolgozat kiválasztása',
        'linkek': list(map(lambda t: { 'nev':  t.nev, 'link':  t.slug}, Dolgozat.objects.filter(osztaly = az_osztaly))),
    }
    return render(request, template, context)


def felhasznalok_regisztracioja(request):
    if not request.user.groups.filter(name='adminisztrator').exists():
        return HttpResponseForbidden()
    template = "app_naplo/userinput.html"
    context = {}
    return render(request, template, context)


def dolgozat(request, group_name, dolgozat_slug):
    if not request.user.groups.filter(name='adminisztrator').exists():
        return HttpResponseForbidden()
    template = "app_naplo/pontinput.html"
    a_group = Group.objects.filter(name=group_name).first()
    if a_group == None:
        return HttpResponseNotFound(f'Ilyen csoport nincs: {group_name}')
    a_dolgozat = Dolgozat.objects.filter(slug=dolgozat_slug, osztaly=a_group).first()
    if a_dolgozat == None:
        return HttpResponseNotFound(f'Ilyen dolgozat nincs: {dolgozat_slug}')
    
    context = {
        'a_dolgozat': a_dolgozat,
    }
    return render(request, template, context)


def dolgozatmatrixeditor(request, group_name, dolgozat_slug):
    if not request.user.groups.filter(name='adminisztrator').exists():
        return HttpResponseForbidden()
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
