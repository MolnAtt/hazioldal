from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .models import Git, Hf, Mentoral, Temakor
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from APP.seged import tagja





@login_required
def index(request: HttpRequest) -> HttpResponse:
    return redirect(f'http://{request.get_host()}/attekintes/hf/uj/')


@login_required
def hazik(request: HttpRequest, hfmo: str, szuro: str) -> HttpResponse:
    mentor_vagyok = hfmo == "mo"
    mentoralt_vagyok = hfmo == "hf"
    if mentor_vagyok:
        hazik = Hf.mentoraltak_hazijainak_unioja(request.user)
    elif mentoralt_vagyok:
        hazik = Hf.sajat_hazijaim(request.user)
    else:
        hazik = []
    return render(request, "hazik.html", { 
        'hazik': Hf.lista_to_template(hazik, request.user),
        'szam' : Hf.mibol_mennyi(request.user),
        'szuro': szuro,
        'mentor_vagyok': mentor_vagyok,
        'mentoralt_vagyok': mentoralt_vagyok,
        })

@login_required
def hf(request:HttpRequest, hfid:int) -> HttpResponse:
    a_hf = Hf.objects.filter(id=hfid).first()
    az_allapot = a_hf.allapot()
    return render(request, "hf.html", {
        'hf': a_hf,
        'mentor_vagyok': Mentoral.ja(request.user, a_hf.user),
        'mentoralt_vagyok': request.user == a_hf.user,
        'uj_megoldast_adhatok_be': az_allapot in ["NINCS_MO", "NINCS_BIRALAT", "VAN_NEGATIV_BIRALAT"],
        'uj_biralatot_rogzithetek': az_allapot not in ["NINCS_REPO", "NINCS_MO"] and not a_hf.et_mar_mentoralta(request.user),
        'megoldasok_es_biralatok': a_hf.megoldasai_es_biralatai(),
    })

@login_required
def fiok(request:HttpRequest) -> HttpResponse:
    return render(request, "fiok.html", {
        'gituser': request.user.git,
    })

@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def regisztracio(request:HttpRequest) -> HttpResponse:
    return render(request, "regisztracio.html", {})


@user_passes_test(lambda user : tagja(user, 'tanar'))
def kituz(request:HttpRequest) -> HttpResponse:
    return render(request, "kituz.html", {
        'temak': Temakor.objects.all().order_by('sorrend'),
        'csoportok': [csoport for csoport in Group.objects.all() if csoport.name[-1]=='f'],
        })


@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def adminisztracio(request:HttpRequest) -> HttpResponse:
    return render(request, "adminisztracio.html", {})


