from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .models import *
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import user_passes_test
from APP.seged import *
from django.utils import timezone
from datetime import datetime
import pytz
import local_settings
from APP.seged import ez_a_tanev, evnyito, kov_evnyito
from github import Github, Auth
import markdown

NINCS_REPO = "NINCS_REPO"
# a mentorált még nem változtatta meg a default repo linket azaz a https://github.com/ -ot.
NINCS_MO = "NINCS_MO"
# a mentoráltnak már van repo-ja, de még nem nyújtott be megoldást rá.
NINCS_BIRALAT = "NINCS_BIRALAT"
# a mentoráltnak már van repoja, van utolsó megoldása, amire viszont még nem kapott bírálatot.
VAN_NEGATIV_BIRALAT = "VAN_NEGATIV_BIRALAT"
# a mentoráltnak már van repoja, van utolsó megoldása és ennek van bírálata is: ezek közt viszont van egy negatív.
MINDEN_BIRALAT_POZITIV = "MINDEN_BIRALAT_POZITIV"
# a mentoráltnak már van repoja, van utolsó megoldása és ennek minden bírálata pozitív.
APP_URL_LABEL = 'hazioldal'

@login_required
def index(request: HttpRequest) -> HttpResponse:
    if tagja(request.user, 'tanar'):
        return redirect('tanar_csoportvalasztas')
    return redirect('mentoralt_ellenorzes')

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

    szam = request.user.git.mibol_mennyi()

    if hfmo+szuro not in szam.keys():
        return SajatResponse(request, "Hibás url", status=404)

    print(f'request.get_host() = {request.get_host()}')
    context = {
        'hazik': Hf.lista_to_template(hazik, request.user),
        'szam' : szam,
        'szuro': szuro,
        'nincs_hazi': 0 == szam[hfmo+szuro],
        'mentor_vagyok': mentor_vagyok,
        'mentoralt_vagyok': mentoralt_vagyok,
        'APP_URL_LABEL' : APP_URL_LABEL,
        }
    return render(request, 'hazik.html', context)

@login_required
def hf(request:HttpRequest, hfid:int) -> HttpResponse:
    a_hf = Hf.objects.filter(id=hfid).first()
    if a_hf == None:
        return SajatResponse(request, "Nincs ilyen házi", status=404)
    if not (request.user == a_hf.user or Mentoral.ja(request.user, a_hf.user) or tagja(request.user, "adminisztrator")):
        return SajatResponse(request, f"Kedves {request.user}, nincs jogosultságod megnézni ezt a házit, mert nem vagy sem admin, sem mentor, sem {a_hf.user}", status=403)

    context = {
        'hf': a_hf,
        'szam' : request.user.git.mibol_mennyi(),
        'mentor_vagyok': Mentoral.ja(request.user, a_hf.user),
        'tanarvagyok': tagja(request.user, 'tanar'),
        'mentoralt_vagyok': request.user == a_hf.user,
        'uj_megoldast_adhatok_be': a_hf.allapot in [NINCS_MO, NINCS_BIRALAT, VAN_NEGATIV_BIRALAT],
        'uj_biralatot_rogzithetek': a_hf.allapot not in [NINCS_REPO, NINCS_MO] and not a_hf.et_mar_mentoralta(request.user),
        'megoldasok_es_biralatok': a_hf.megoldasai_es_biralatai(a_hf.url),
        'github_key' : Git.objects.filter(user=request.user).first().github_token,
        'APP_URL_LABEL' : APP_URL_LABEL,
    }
    return render(request, 'hf.html', context)

@login_required
def ujhf(request:HttpRequest, hfid:int) -> HttpResponse:
    a_hf = Hf.objects.filter(id=hfid).first()
    if a_hf == None:
        return SajatResponse(request, "Nincs ilyen házi", status=404)
    if not (request.user == a_hf.user or Mentoral.ja(request.user, a_hf.user) or tagja(request.user, "adminisztrator")):
        return SajatResponse(request, f"Kedves {request.user}, nincs jogosultságod megnézni ezt a házit, mert nem vagy sem admin, sem mentor, sem {a_hf.user}", status=403)

    megoldasok_es_biralatok = a_hf.megoldasai_es_biralatai(a_hf.url)
    csak_megoldasok = Mo.objects.filter(hf=a_hf)

    utolso_hataridoben = csak_megoldasok.earliest('ido').ido < a_hf.hatarido if csak_megoldasok.exists() else timezone.now() < a_hf.hatarido

    context = {
        # Context
        'hf': a_hf,
        'hazi_halasztva': a_hf.hatarido.date() != a_hf.kituzes.hatarido.date(),
        'mentorok': Mentoral.oi(a_hf.user),
        'hazik': Hf.objects.filter(user=a_hf.user).exclude(id=a_hf.id), # kiveve a_hf
        # Boolean filters
        'mentor_vagyok': Mentoral.ja(request.user, a_hf.user),
        'tanar_vagyok': tagja(request.user, 'tanar'),
        'mentoralt_vagyok': request.user == a_hf.user,
        'van_mar_megoldas': csak_megoldasok.exists(),
        # Boolean actions
        'uj_megoldast_adhatok_be': a_hf.allapot in [NINCS_MO, NINCS_BIRALAT, VAN_NEGATIV_BIRALAT],
        'uj_biralatot_rogzithetek': a_hf.allapot not in [NINCS_REPO, NINCS_MO] and not a_hf.et_mar_mentoralta(request.user),
        # Chat
        'messages': megoldasok_es_biralatok,
        # GitHub Commit History Beta
        'github_key' : Git.objects.filter(user=request.user).first().github_token,
        # Assist
        'APP_URL_LABEL' : APP_URL_LABEL,
        'hataridoben_van': utolso_hataridoben,
    }

    return render(request, 'ujhf.html', context)

def SajatResponse(request:HttpRequest, uzenet:str="", status:int=None) -> HttpResponse:
    # hibakezelés, ha fura kwargs argumentumot adnak meg
    template='sajathibauzenet.html'
    context={
        'uzenet':uzenet,
        'status':status
        #'statuscode':kwargs['status'], #??
        }
    return render(request, template, context)

@login_required
def haladek(request:HttpRequest, haladekid:int) -> HttpResponse:
    a_haladekkerelem = Haladek_kerelem.objects.filter(id=haladekid).first()
    a_hf = Hf.objects.filter(id=a_haladekkerelem.hf.id).first()
    if a_hf == None:
        return SajatResponse(request, "Nincs ilyen házi", status=404)
    if not (request.user == a_hf.user or tagja(request.user, "adminisztrator")):
        return SajatResponse(request, f"Kedves {request.user}, nincs jogosultságod megnézni ezt a házit, mert nem vagy sem admin sem {a_hf.user}", status=403)
    context = {
        'a_hf': a_hf,
        'a_haladekkerelem': a_haladekkerelem,
    }
    return render(request, 'haladek_view.html', context)

@login_required
def haladekopciok(request:HttpRequest, hfid:int) -> HttpResponse:
    a_hf = Hf.objects.filter(id=hfid).first()
    if a_hf == None:
        return SajatResponse(request)
    if not (request.user == a_hf.user or tagja(request.user, "adminisztrator")):
        return SajatResponse(request, f"Kedves {request.user}, nincs jogosultságod megnézni ezt a házit, mert nem vagy sem admin sem {a_hf.user}", status=403)

    context = {
        "mentor": True if Mentoral.tjai(request.user) else False,
    }

    return render(request, 'haladekopciok.html', context)

@login_required
def haladekok(request: HttpRequest) -> HttpResponse:

    if not (tagja(request.user, "tanar") or tagja(request.user, "adminisztrator")):
        user_haladek_kerelmei = Haladek_kerelem.objects.filter(hf__user=request.user)
    else:
        user_haladek_kerelmei = Haladek_kerelem.objects.all()

    fuggok = user_haladek_kerelmei.filter(elbiralva="fuggo")
    elfogadottak = user_haladek_kerelmei.filter(elbiralva="elfogadott")
    elutasitottak = user_haladek_kerelmei.filter(elbiralva="elutasitott")

    context = {
        "fuggok": fuggok,
        "elfogadottak": elfogadottak,
        "elutasitottak": elutasitottak,
    }

    return render(request, 'haladekok.html', context)

@login_required
def haladek_torol(request:HttpRequest, haladekid:int) -> HttpResponse:
    a_haladek_kerelem = Haladek_kerelem.objects.filter(id=haladekid).first()

    if a_haladek_kerelem == None:
        return SajatResponse(request, "Nincs ilyen haladékkérelem", status=404)
    if not (request.user == a_haladek_kerelem.hf.user or tagja(request.user, "adminisztrator")):
        return SajatResponse(request, f"Kedves {request.user}, nincs jogosultságod törölni ezt a haladékkérelmet, mert nem vagy sem admin sem {a_haladek_kerelem.user}", status=403)

    a_haladek_kerelem.delete()

    return redirect("haladekok")

@login_required
def haladek_egyeb_post(request:HttpRequest, hfid:int, tipus:str) -> HttpResponse:
    if request.method != "POST":
        return SajatResponse(request, "Ezt az oldalt csak a megfelelő form kitöltésével lehet elérni", status=403)
    a_hf = Hf.objects.filter(id=hfid).first()
    if a_hf == None:
        return SajatResponse(request, "Nincs ilyen házi", status=404)
    if tipus not in ["hianyzas", "egyeb"]:
        return SajatResponse(request, "Nincs ilyen haladékkérelem típus", status=404)
    if not (request.user == a_hf.user or tagja(request.user, "adminisztrator")):
        return SajatResponse(request, f"Kedves {request.user}, nincs jogosultságod ilyen kérelmet leadni.", status=403)

    a_haladek_kerelem = Haladek_kerelem.objects.create(
        tipus = tipus,
        targy = tipus,
        body = request.POST["indoklas"],
        hf = a_hf,
        nap = request.POST["napszam"],
        valasz = '-',
    )

    return redirect("haladekok")

@login_required
def haladek_elfogad(request: HttpRequest, haladekid:int) -> HttpResponse:
    if request.method != "POST":
        return SajatResponse(request, "Ezt az oldalt csak a megfelelő form kitöltésével lehet elérni", status=403)
    hk = Haladek_kerelem.objects.filter(id=haladekid).first()
    if hk == None:
        return SajatResponse(request, "Nincs ilyen haladákkérelem", status=404)
    
    if not (tagja(request.user, "tanar") or tagja(request.user, "adminisztrator")):
        return SajatResponse(request, f"Kedves {request.user}, nincs jogosultságod ilyen kérelmet leadni.", status=403)
    
    hk.apporove()

    return redirect("haladekok")


@login_required
def haladek_fuggeszt(request: HttpRequest, haladekid:int) -> HttpResponse:
    if request.method != "POST":
        return SajatResponse(request, "Ezt az oldalt csak a megfelelő form kitöltésével lehet elérni", status=403)
    hk = Haladek_kerelem.objects.filter(id=haladekid).first()
    if hk == None:
        return SajatResponse(request, "Nincs ilyen haladákkérelem", status=404)
    
    if not (tagja(request.user, "tanar") or tagja(request.user, "adminisztrator")):
        return SajatResponse(request, f"Kedves {request.user}, nincs jogosultságod ilyen kérelmet leadni.", status=403)
    
    hk.toPending()

    return redirect("haladekok")


@login_required
def haladek_elutasit(request: HttpRequest, haladekid:int) -> HttpResponse:
    if request.method != "POST":
        return SajatResponse(request, "Ezt az oldalt csak a megfelelő form kitöltésével lehet elérni", status=403)
    hk = Haladek_kerelem.objects.filter(id=haladekid).first()
    if hk == None:
        return SajatResponse(request, "Nincs ilyen haladákkérelem", status=404)
    
    if not (tagja(request.user, "tanar") or tagja(request.user, "adminisztrator")):
        return SajatResponse(request, f"Kedves {request.user}, nincs jogosultságod ilyen kérelmet leadni.", status=403)
    
    hk.deny()

    return redirect("haladekok")


@login_required
def haladek_mentoralas_post(request:HttpRequest, hfid:int) -> HttpResponse:
    if request.method != "POST":
        return SajatResponse(request, "Ezt az oldalt csak a megfelelő form kitöltésével lehet elérni", status=403)
    a_hf = Hf.objects.filter(id=hfid).first()
    if a_hf == None:
        return SajatResponse(request, "Nincs ilyen házi", status=404)
    if not (request.user == a_hf.user or tagja(request.user, "adminisztrator")):
        return SajatResponse(request, f"Kedves {request.user}, nincs jogosultságod ilyen kérelmet leadni.", status=403)

    print(request.POST)

    a_biralat = Biralat.objects.filter(id=request.POST['biralatid']).first()
    if a_biralat == None:
        return SajatResponse(request, "Nincs ilyen response biralat", status=404)

    a_haladek_kerelem = Haladek_kerelem.objects.create(
        tipus = "mentoralas",
        targy = "Haladékkérelem mentorálással",
        biralat = a_biralat,
        body = f"A {request.user} felhasználó a következő házi feladatára szeretne {request.POST['napszam']} nap haladékot kérni. Ehhez a következő bírálatra hivatkozik: HF{a_biralat.mo.hf.id} (Bírálat - {a_biralat.id}) https://{request.get_host()}/hazioldal/hf/{a_biralat.mo.hf.id}/",
        hf = a_hf,
        nap = request.POST["napszam"],
    )

    return redirect("haladekok")

@login_required
def haladek_egyeb(request:HttpRequest, hfid:int, tipus:str) -> HttpResponse:
    a_hf = Hf.objects.filter(id=hfid).first()
    if a_hf == None:
        return SajatResponse(request, "Nincs ilyen házi", status=404)
    if not (request.user == a_hf.user or tagja(request.user, "adminisztrator")):
        return SajatResponse(request, f"Kedves {request.user}, nincs jogosultságod megnézni ezt a házit, mert nem vagy sem admin sem {a_hf.user}", status=403)
    context = {
        'tipus': tipus,
        'a_hf': a_hf,
        'default': '... napig hiányoztam, ezért szeretnék haladékot kérni.' if tipus == 'hianyzas' else '...',
    }
    return render(request, 'haladek_egyeb.html', context)

@login_required
def haladek_mentoralas(request:HttpRequest, hfid:int) -> HttpResponse:
    a_hf = Hf.objects.filter(id=hfid).first()
    if a_hf == None:
        return SajatResponse(request, "Nincs ilyen házi", status=404)
    if not (request.user == a_hf.user or tagja(request.user, "adminisztrator")):
        return SajatResponse(request, f"Kedves {request.user}, nincs jogosultságod megnézni ezt a házit, mert nem vagy sem admin sem {a_hf.user}", status=403)
    context = {
        'tipus': "Mentorálás",
        'a_hf': a_hf,
        'mentoraltak': Mentoral.tjai(request.user),
    }
    return render(request, 'haladek_mentoralas.html', context)

@login_required
def fiok(request:HttpRequest) -> HttpResponse:
    kozszolg_percek = sum(biralat.kozossegi_szolgalati_percek for biralat in Biralat.objects.filter(mentor=request.user).exclude(kozossegi_szolgalati_percek=-1))
    if kozszolg_percek < 0:
        kozszolg_percek = 0
    context = {
        'gituser': request.user.git,
        'commithistory': request.user.git.commithistory,
        'szam' : request.user.git.mibol_mennyi(),
        'APP_URL_LABEL' : APP_URL_LABEL,
        'kozszolg_percek': kozszolg_percek,
        'vannak_kozszolg_percek': 0 < kozszolg_percek,
        'van_konyvelheto_ora': kozszolg_percek % 60 > 0,
        }
    return render(request, 'fiok.html', context)

@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def regisztracio(request:HttpRequest) -> HttpResponse:
    context = {
        'szam' : request.user.git.mibol_mennyi(),
        'APP_URL_LABEL' : APP_URL_LABEL,
    }
    return render(request, 'regisztracio.html', context)

@user_passes_test(lambda user : tagja(user, 'tanar'))
def kituz(request:HttpRequest) -> HttpResponse:
    context = {
        'temak': Temakor.objects.all().order_by('sorrend'),
        'szam' : request.user.git.mibol_mennyi(),
        'csoportok': Group.objects.all(),
        'APP_URL_LABEL' : APP_URL_LABEL,
        }
    return render(request, 'kituz.html', context)

@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def adminisztracio(request:HttpRequest) -> HttpResponse:
    context = {
        'csoportok': Group.objects.all(),
        'szam' : request.user.git.mibol_mennyi(),
        'APP_URL_LABEL' : APP_URL_LABEL,
        'biralatok': Biralat.objects.filter(kozossegi_szolgalati_percek=-1).exclude(mentor__groups__name='tanar')[:1]
    }
    return render(request, 'adminisztracio.html', context)

@user_passes_test(lambda user : tagja(user, 'tanar'))
def ellenorzes_csoportvalasztas_tanarnak(request:HttpRequest) -> HttpResponse:
    csoportok = sorted([t.csoport for t in Tanit.objects.filter(tanar = request.user)], key=lambda l: l.name)
    context = {
        'csoportok': csoportok,
        'szam' : request.user.git.mibol_mennyi(),
        'APP_URL_LABEL' : APP_URL_LABEL,
        'mentor_vagy_tanar': 'tanar',
        }
    return render(request, 'ellenorzes_csoportvalasztas.html', context)

def ellenorzes_csoportvalasztas_mentornak(request: HttpRequest) -> HttpResponse:
    csoportok = set()
    for mentoralt in Mentoral.tjai(request.user):
        for g in mentoralt.groups.all():
            csoportok.add(g)

    context = {
        'csoportok': csoportok,
        'szam': request.user.git.mibol_mennyi(),
        'APP_URL_LABEL': APP_URL_LABEL,
        'mentor_vagy_tanar': 'mentor',
    }

    if len(csoportok) == 1:
        context['redirected'] = True
        csoport_list = list(csoportok)
        return redirect(f'/hazioldal/{context["mentor_vagy_tanar"]}/ellenorzes/{csoport_list[0].name}')

    return render(request, 'ellenorzes_csoportvalasztas.html', context)


@user_passes_test(lambda user : tagja(user, 'tanar'))
def ellenorzes_tanarnak(request:HttpRequest, csoport:str) -> HttpResponse:
    a_group = Group.objects.filter(name=csoport).first()
    if a_group==None:
        return SajatResponse(request, 'ilyen csoport nincs')
    a_userek = User.objects.filter(groups__name=a_group.name)#.order_by('last_name', 'first_name')
    ettol = aktualis_tanev_eleje()
    a_csoport_kituzesei = [ k for k in Kituzes.objects.filter(group=a_group) if ettol <= timezone.make_aware(k.ido) ]


    # mehetne modellbe idáig!
    context = {
        'kituzesek_szama': len(a_csoport_kituzesei),
        'kituzesek': a_csoport_kituzesei,
        'userek': a_userek,
        'userek_sorai': Hf.kockaview(a_userek, a_csoport_kituzesei),
        'szam' : request.user.git.mibol_mennyi(),
        'APP_URL_LABEL' : APP_URL_LABEL,
        'tanarvagyok': tagja(request.user, 'tanar'),
        'csoportnev': csoport,
        }
    return render(request, 'ellenorzes.html', context)

@login_required
def ellenorzes_mentoraltnak(request:HttpRequest) -> HttpResponse:
    a_user = request.user
    ettol = aktualis_tanev_eleje()
    a_group = a_user.groups.first()
    a_csoport_kituzesei = [ k for k in Kituzes.objects.filter(group=a_group) if ettol <= k.ido ]

    context = {
        'kituzesek_szama': len(a_csoport_kituzesei),
        'kituzesek': a_csoport_kituzesei,
        'userek': [a_user],
        'userek_sorai': Hf.kockaview([a_user], a_csoport_kituzesei),
        'szam' : request.user.git.mibol_mennyi(),
        'APP_URL_LABEL' : APP_URL_LABEL,
        'tanarvagyok': tagja(request.user, 'tanar'),
        'csoportnev': a_group.name,
        }
    return render(request, 'ellenorzes.html', context)

@login_required
def hazinezet(request:HttpRequest) -> HttpResponse:
    a_user = request.user
    ettol = aktualis_tanev_eleje()
    a_group = a_user.groups.first()

    iden = ez_a_tanev()
    a_user_kituzesei = Hf.objects.filter(user=a_user, hatarido__range=(timezone.make_aware(evnyito(iden)), timezone.make_aware(kov_evnyito(iden))))

    hetiview_results = Hf.hetiview(a_user_kituzesei)

    context = {
        'hetiview_results': hetiview_results,
        # 'hetiview_results': {6: [Hf.objects.filter(user = request.user).first()]},
        'szam': request.user.git.mibol_mennyi(),
        'APP_URL_LABEL': APP_URL_LABEL,
        'tanarvagyok': tagja(request.user, 'tanar'),
        'mentorvagyok': Mentoral.e(a_user),
        'csoportnev': a_group.name,
        'van_beavatkozos': 0 < len(a_user_kituzesei.filter(allapot=VAN_NEGATIV_BIRALAT)),
}

    return render(request, "hazinezet.html", context)

@login_required
def ellenorzes_mentornak(request:HttpRequest, csoport:str) -> HttpResponse:
    a_group = Group.objects.filter(name=csoport).first()
    if a_group==None:
        return SajatResponse(request, 'ilyen csoport nincs')
    a_userek = [ u for u in Mentoral.tjai(request.user) if u in a_group.user_set.all()]
    ettol = aktualis_tanev_eleje()
    a_csoport_kituzesei = [ k for k in Kituzes.objects.filter(group=a_group) if ettol <= k.ido ]

    # mehetne modellbe idáig!
    context = {
        'kituzesek_szama': len(a_csoport_kituzesei),
        'kituzesek': a_csoport_kituzesei,
        'userek': a_userek,
        'userek_sorai': Hf.kockaview(a_userek, a_csoport_kituzesei),
        'szam' : request.user.git.mibol_mennyi(),
        'APP_URL_LABEL' : APP_URL_LABEL,
        'tanarvagyok': tagja(request.user, 'tanar'),
        'csoportnev': csoport,
        }

    return render(request, 'ellenorzes.html', context)

@login_required
def uj_mentor_ellenorzes(request:HttpRequest, csoport:str) -> HttpResponse:
    a_group = Group.objects.filter(name=csoport).first()
    if a_group==None:
        return SajatResponse(request, 'ilyen csoport nincs')
    a_userek = [
        u for u in Mentoral.tjai(request.user) if u.groups.filter(name=csoport).exists()
        ]
    a_userek_mentorai = [Mentoral.oi(user) for user in a_userek]
    a_csoport_kituzesei = [ k for k in Kituzes.objects.filter(group=a_group, ido__gte=aktualis_tanev_eleje()) ]

    for i, user in enumerate(a_userek):
        user.mentorai = a_userek_mentorai[i]

    context = {
        'kituzesek_szama': len(a_userek)+1,
        'kituzesek': a_csoport_kituzesei,
        'userek': a_userek,
        'kituzesek_sorai': Hf.new_mentorview(a_userek, a_csoport_kituzesei),
        'APP_URL_LABEL' : APP_URL_LABEL,
        'tanarvagyok': tagja(request.user, 'tanar'),
        'csoportnev': csoport,
    }
    return render(request, 'uj_mentor_ellenorzes.html', context)


@login_required
def uj_tanar_ellenorzes_redirect(request:HttpRequest, csoport:str) -> HttpResponse:
    ev1, ev2 = idopont_evparja(ovatos_timezone_awareness(timezone.now()))
    return redirect(f'/hazioldal/tanar/ellenorzes/{ev1}/{ev2}/{csoport}/')


@login_required
def uj_tanar_ellenorzes(request:HttpRequest, ev1:int, ev2:int, csoport:str) -> HttpResponse:
    a_group = Group.objects.filter(name=csoport).first()
    if a_group==None:
        return SajatResponse(request, 'ilyen csoport nincs')
    a_userek = [
        u for u in Mentoral.tjai(request.user) if u.groups.filter(name=csoport).exists()
        ]
    a_userek_mentorai = [Mentoral.oi(user) for user in a_userek]

    a_csoport_kituzesei = [ k for k in Kituzes.objects.filter(group=a_group, ido__gte=szept_1(ev1), ido__lte=aug_31(ev2)) ]

    for i, user in enumerate(a_userek):
        user.mentorai = a_userek_mentorai[i]

    context = {
        'kituzesek_szama': len(a_userek)+1,
        'kituzesek': a_csoport_kituzesei,
        'userek': a_userek,
        'kituzesek_sorai': Hf.new_mentorview(a_userek, a_csoport_kituzesei),
        'APP_URL_LABEL' : APP_URL_LABEL,
        'tanarvagyok': tagja(request.user, 'tanar'),
        'csoportnev': csoport,
    }
    return render(request, 'uj_mentor_ellenorzes.html', context)



@login_required
@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def kampany(request:HttpResponse, kampanyid:int) -> HttpResponse:
    if not(a_kampany := Kampany.objects.filter(id=kampanyid).first()):
        return HttpResponse('nincs ilyen id-val kampány')
    return render(request, 'kampany.html', {'a_kampany':a_kampany})


