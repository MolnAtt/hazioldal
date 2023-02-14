from tokenize import group
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .models import Dolgozat
from APP.models import Tanit
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound,  HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test, login_required
from APP.seged import tagja

@login_required
def index(request):
    if not tagja(request.user, 'tanar'):
        return tanulo_redirect(request)
    
    template='app_naplo/valaszto.html'
    context={
        'cim': 'Napló',
        'linkek' : [
            { 'nev':  'Csoport regisztrációja', 'link':  'regisztracio'},
            { 'nev':  'Csoport kiválasztása', 'link':  'csoport'},
            ],
    }
    return render(request, template, context)


@login_required
@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def csoportvalaszto(request):
    template = "app_naplo/valaszto.html"
    context = {
        'cim': 'Osztály kiválasztása',
        'linkek': sorted([{ 'nev':  t.csoport.name, 'link':  t.csoport.name} for t in Tanit.objects.filter(tanar = request.user)], key=lambda l: l['nev']),
    }
    return render(request, template, context)

@login_required
@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def ujdolgozat(request, group_name):
    az_osztaly = Group.objects.filter(name=group_name).first()
    if az_osztaly==None:
        return HttpResponseNotFound(f"ilyen osztály nincs: {group_name}")
    
    context = {}
    context['az_osztaly'] = az_osztaly
    template = "app_naplo/ujdolgozat.html"
    return render(request, template, context)

@login_required
@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def dolgozatvalaszto(request, group_name):
    template = "app_naplo/valaszto.html"
    
    az_osztaly = Group.objects.filter(name=group_name).first()
    if az_osztaly==None:
        return HttpResponseNotFound(f"ilyen osztály nincs: {group_name}")

    context = {
        'cim': 'Dolgozat kiválasztása',
        'linkek': [{ 'nev':  d.nev, 'link':  d.slug} for d in Dolgozat.objects.filter(osztaly = az_osztaly)]
                    +[ { 'nev': 'Új dolgozat', 'link':  'uj_dolgozat'}],
    }
    return render(request, template, context)

@login_required
def tanulo_redirect(request):
    return redirect(f'http://{request.get_host()}/naplo/tanulo/{request.user.id}/')

@login_required
def tanuloi_dolgozatvalaszto(request, tanuloid):
    if request.user.id != tanuloid and not tagja(request.user, 'adminisztrator'): # kukkolás
        return redirect(f'http://{request.get_host()}/naplo/tanulo/{request.user.id}/')
    
    linkek = []
    for csoport in request.user.groups.all():
        for dolgozat in Dolgozat.objects.filter(osztaly=csoport):
            linkek.append({
                'nev':  dolgozat.nev,
                'link':  dolgozat.slug,
                })
            
    template = "app_naplo/valaszto.html"
    context = {
        'cim': 'Dolgozat kiválasztása',
        'linkek': linkek,
    }
    return render(request, template, context)

@login_required
def tanuloi_kimutatas(request, tanuloid, dolgozat_slug):
    if request.user.id != tanuloid and not tagja(request.user, 'adminisztrator'): # kukkolás
        return redirect(f'https://{request.get_host()}/naplo/tanulo/{request.user.id}/')
    
    a_dolgozat = Dolgozat.objects.filter(slug=dolgozat_slug).first()
    sorok = a_dolgozat.json(request.user)
    print(sorok)            
    
    template = "app_naplo/tanulo_dolgozata.html"
    context = {
        'a_user': request.user,
        'a_dolgozat': a_dolgozat,
        'sorok' : sorok,
        'dolgozat': a_dolgozat,
        'csoportok': list(request.user.groups.values_list('name', flat = True)),
    }
    return render(request, template, context)


@login_required
@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def felhasznalok_regisztracioja(request):
    template = "app_naplo/userinput.html"
    context = {}
    return render(request, template, context)


@login_required
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
        'dolgozatszotar': a_dolgozat.szotar(),
        'ertekeloszotar': a_dolgozat.ertekeloszotar(),
        'jegy': 'jegy',
        'szazalek': 'szazalek',
        'pont': 'pont',
        'atlagok': a_dolgozat.osszesites(Dolgozat.atlag),
        'medianok': a_dolgozat.osszesites(Dolgozat.median),
        'minimumok': a_dolgozat.osszesites(Dolgozat.minimum),
        'maximumok': a_dolgozat.osszesites(Dolgozat.maximum),
        }
    return render(request, template, context)
   

@login_required
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



@login_required
@user_passes_test(lambda user : tagja(user, 'tanar'))
def dolgozat_download(request, group_name, dolgozat_slug):
    a_group = Group.objects.filter(name=group_name).first()
    if a_group == None:
        return HttpResponseNotFound(f'Ilyen csoport nincs: {group_name}')
    
    a_dolgozat = Dolgozat.objects.filter(slug=dolgozat_slug, osztaly=a_group).first()
    if a_dolgozat == None:
        return HttpResponseNotFound(f'Ilyen dolgozat nincs: {dolgozat_slug}')
    
    return HttpResponse(serializers.serialize("json", Dolgozat.objects.filter(id = a_dolgozat.id)))
