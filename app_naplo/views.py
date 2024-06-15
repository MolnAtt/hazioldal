from tokenize import group
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .models import Dolgozat, Lezaras 
from APP.models import Egyes
from APP.models import Tanit
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound,  HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test, login_required
from APP.seged import tagja, ez_a_tanev, evnyito, kov_evnyito
from datetime import datetime
from django.utils.timezone import make_aware

magyarhonapnev=['jan', 'feb', 'márc', 'ápr', 'máj', 'jún', 'júl', 'aug', 'szept', 'okt', 'nov', 'dec']

def magyardatum(d):
    return f'{magyarhonapnev[d.month-1]}. {"{:02d}".format(d.day)}.'

def index(request):
    if not tagja(request.user, 'tanar'):
        return tanulo_redirect(request, ez_a_tanev())    
    return redirect(f'http://{request.get_host()}/naplo/{ez_a_tanev()}/csoport/')

def index_ev(request, ev:int):
    return index(request)

# @user_passes_test(lambda user : tagja(user, 'adminisztrator'))
@login_required
def csoportvalaszto(request, ev):
    if not tagja(request.user, 'tanar'):
        return tanulo_redirect(request, ez_a_tanev())
    template = "app_naplo/t_1_naplo_csoportvalaszto.html"
    context = {
        'cim': 'Osztály kiválasztása',
        'linkek': sorted([{ 'nev':  t.csoport.name, 'link':  t.csoport.name} for t in Tanit.objects.filter(tanar = request.user)], key=lambda l: l['nev']),
    }
    return render(request, template, context)

@login_required
@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def ujdolgozat(request, ev, group_name):
    az_osztaly = Group.objects.filter(name=group_name).first()
    if az_osztaly==None:
        return HttpResponseNotFound(f"ilyen osztály nincs: {group_name}")
    
    context = {
        'az_osztaly':az_osztaly,
        'ev': ev,
    }
    return render(request, 'app_naplo/t_2_ujdolgozat.html', context)

@login_required
@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def dolgozatvalaszto(request, ev, group_name):
    
    az_osztaly = Group.objects.filter(name=group_name).first()
    if az_osztaly==None:
        return HttpResponseNotFound(f"ilyen osztály nincs: {group_name}")

    
    tanulok = az_osztaly.user_set.all().order_by('last_name', 'first_name')
    mettol = evnyito(ev) 
    meddig = kov_evnyito(ev)
    dolgozatok = list(Dolgozat.objects.filter(osztaly = az_osztaly, datum__range=(mettol, meddig)).order_by('datum'))


    lezaras_mettol_meddig = Lezaras.aktualis_intervallum_megallapitasa()

    sorok =  [{
        'tanulo': tanulo,
        'ertekelesek': [dolgozat.ertekeles(tanulo) for dolgozat in dolgozatok],
        'osszesites': Dolgozat.ok_alapjan_igy_all(tanulo, az_osztaly, mettol, meddig),
        'lezaras': Lezaras.objects.filter(tanulo=tanulo, csoport=az_osztaly, datum__range=lezaras_mettol_meddig).first()
        } for tanulo in tanulok]
        
        
    context = {
        'ev': ev,
        'csoport': az_osztaly,
        'tanulok': tanulok,
        'dolgozatok': dolgozatok, 
        'sorok': sorok,
    }
    return render(request, 'app_naplo/t_2_csoportnaplo.html', context)

@login_required
def tanulo_redirect(request, ev):
    return redirect(f'http://{request.get_host()}/naplo/{ev}/tanulo/{request.user.id}/')

@login_required
def ellenorzo(request, ev, tanuloid, group_name):
    if request.user.id != tanuloid and not tagja(request.user, 'adminisztrator'): # kukkolás
        return redirect(f'http://{request.get_host()}/naplo/tanulo/{request.user.id}/')
    
    a_user = User.objects.filter(id=tanuloid).first()
    if a_user==None:
        return HttpResponseNotFound(f'Ilyen id-val nincs user: {tanuloid}')
    
    a_group = Group.objects.filter(name=group_name).first()
    if a_group == None:
        return HttpResponseNotFound(f'Ilyen csoport nincs: {group_name}')

    mettol = make_aware(evnyito(ev)) 
    meddig = make_aware(kov_evnyito(ev))


    dolgozatok = Dolgozat.objects.filter(osztaly=a_group, datum__range=(mettol, meddig))
    ertekelesek = [szotar_unio({
        'nev': dolgozat.nev, 
        'dolgozat_e': True,
        'slug': f'naplo/{ev}/tanulo/{tanuloid}/dolgozat/{dolgozat.slug}/',
        'suly': dolgozat.suly,
        'sulyvektor': dolgozat.sulyvektor,
        'matrixbeli_sorszam': dolgozat.matrixaban_tanulo_sorindexe(a_user)
        'datum': dolgozat.date(), # a sorbarendezés miatt kell
        'datumszoveg': magyardatum(dolgozat.date()),
        'maxpont':sum(dolgozat.feladatmaximumok),
        }, dolgozat.ertekeles(a_user)) for dolgozat in dolgozatok]
    egyesek = [{
        'nev': 'hf: ' + egyes.hf.kituzes.feladat.nev,
        'dolgozat_e': False,
        'slug': f'hazioldal/hf/{egyes.hf.id}/',
        'suly':'0.5',
        'egyeni_suly': egyes.suly,
        'datum': egyes.date(), # a sorbarendezés miatt kell
        'datumszoveg': magyardatum(egyes.date()),
        'pont':'-',
        'maxpont':'-',
        '%':'-',
        'jegy':'1',
        } for egyes in Egyes.ei_egy_tanulonak(a_user, mettol, meddig)]
    sorok = sorted(ertekelesek+egyesek, key= lambda x: x['datum'])  
    


    context = {
        'tanulo': a_user,
        'csoport': a_group,
        'sorok': sorok,
        'osszegzes': Dolgozat.ok_alapjan_igy_all(a_user, a_group, mettol, meddig)
        }
    return render(request, 'app_naplo/d_2_ellenorzo.html', context)

@login_required
def ellenorzo_csoportvalaszto(request, ev, tanuloid):
    if request.user.id != tanuloid and not tagja(request.user, 'adminisztrator'): # kukkolás
        return redirect(f'http://{request.get_host()}/naplo/tanulo/{request.user.id}/')
    
    linkek = [{
        'nev' : csoport.name,
        'link': 'csoport/' + csoport.name,
        } for csoport in request.user.groups.all()]

    context = {
        'cim'   : 'Csoport kiválasztása',
        'linkek': linkek,
    }

    if len(context['linkek']) == 1:
        context["redirected"] = True
        return redirect(context["linkek"][0]["link"])
    
    return render(request, 'app_naplo/d_1_ellenorzo_csoportvalaszto.html', context)

@login_required
def tanulo_dolgozata(request, ev, tanuloid, dolgozat_slug):
    if request.user.id != tanuloid and not tagja(request.user, 'adminisztrator'): # kukkolás
        return redirect(f'https://{request.get_host()}/naplo/tanulo/{request.user.id}/')
    
    a_user = User.objects.filter(id=tanuloid).first()
    if a_user == None:
        return HttpResponseNotFound(f'Ilyen id-val user nincs: {tanuloid}')
    
    a_dolgozat = Dolgozat.objects.filter(slug=dolgozat_slug).first()
    if a_dolgozat == None:
        return HttpResponseNotFound(f'Ilyen dolgozat nincs: {dolgozat_slug}')   

         
    sorok = a_dolgozat.json(a_user)
    
    context = {
        'a_user': a_user,
        'a_dolgozat': a_dolgozat,
        'sorok' : sorok,
        'csoportok': list(a_user.groups.values_list('name', flat = True)),
    }
    return render(request, 'app_naplo/d_3_tanulo_dolgozata.html', context)


@login_required
@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def felhasznalok_regisztracioja(request, ev:int):
    template = "app_naplo/userinput.html"
    context = {}
    return render(request, template, context)


@login_required
@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def dolgozat(request, ev:int, group_name, dolgozat_slug):
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
def dolgozatmatrixeditor(request, ev, group_name, dolgozat_slug):
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
def dolgozat_download(request, ev, group_name, dolgozat_slug):
    a_group = Group.objects.filter(name=group_name).first()
    if a_group == None:
        return HttpResponseNotFound(f'Ilyen csoport nincs: {group_name}')
    
    a_dolgozat = Dolgozat.objects.filter(slug=dolgozat_slug, osztaly=a_group).first()
    if a_dolgozat == None:
        return HttpResponseNotFound(f'Ilyen dolgozat nincs: {dolgozat_slug}')
    
    return HttpResponse(serializers.serialize("json", Dolgozat.objects.filter(id = a_dolgozat.id)))


def szotar_unio(d1, d2): 
    '''
    python 3.8-ban még nem volt ilyen, a házioldal viszont sajnos még abban van.
    '''
    result = {}
    
    for k in d1.keys():
        result[k] = d1[k]
        
    for k in d2.keys():
        result[k] = d2[k]
    
    return result
    