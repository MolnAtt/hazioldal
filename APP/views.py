from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .models import Git, Hf, Mentoral, Temakor, Tanit, Kituzes
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import user_passes_test
from APP.seged import tagja
from django.utils import timezone
from datetime import datetime
import pytz
import local_settings


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
    return redirect(f'http://{request.get_host()}/{APP_URL_LABEL}/attekintes/hf/uj/')

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
        return HttpResponse("Hibás url", status=404)

    template = "hazik.html"
    context = { 
        'hazik': Hf.lista_to_template(hazik, request.user),
        'szam' : szam,
        'szuro': szuro,
        'nincs_hazi': 0 == szam[hfmo+szuro],
        'mentor_vagyok': mentor_vagyok,
        'mentoralt_vagyok': mentoralt_vagyok,
        'APP_URL_LABEL' : APP_URL_LABEL,
        }
    return render(request, template, context)

@login_required
def hf(request:HttpRequest, hfid:int) -> HttpResponse:
    a_hf = Hf.objects.filter(id=hfid).first()
    if a_hf == None:
        return HttpResponse("Nincs ilyen házi", status=404)
    if not (request.user == a_hf.user or Mentoral.ja(request.user, a_hf.user) or tagja(request.user, "adminisztrator")):
        return HttpResponse(f"Kedves {request.user}, nincs jogosultságod megnézni ezt a házit, mert nem vagy sem admin, sem mentor, sem {a_hf.user}", status=403)
    

    template = "hf.html"
    context = {
        'hf': a_hf,
        'szam' : request.user.git.mibol_mennyi(),
        'mentor_vagyok': Mentoral.ja(request.user, a_hf.user),
        'mentoralt_vagyok': request.user == a_hf.user,
        'uj_megoldast_adhatok_be': a_hf.allapot in [NINCS_MO, NINCS_BIRALAT, VAN_NEGATIV_BIRALAT],
        'uj_biralatot_rogzithetek': a_hf.allapot not in [NINCS_REPO, NINCS_MO] and not a_hf.et_mar_mentoralta(request.user),
        'megoldasok_es_biralatok': a_hf.megoldasai_es_biralatai(),
        'github_key' : local_settings.GITHUB_KEY,
        'APP_URL_LABEL' : APP_URL_LABEL,
    }
    return render(request, template, context)

@login_required
def fiok(request:HttpRequest) -> HttpResponse:
    template = "fiok.html"
    context = {
        'gituser': request.user.git,
        'szam' : request.user.git.mibol_mennyi(),
        'APP_URL_LABEL' : APP_URL_LABEL,
        }
    return render(request, template, context)

@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def regisztracio(request:HttpRequest) -> HttpResponse:
    template = "regisztracio.html"
    context = {
        'szam' : request.user.git.mibol_mennyi(),
        'APP_URL_LABEL' : APP_URL_LABEL,
    }
    return render(request, template, context)

@user_passes_test(lambda user : tagja(user, 'tanar'))
def kituz(request:HttpRequest) -> HttpResponse:
    template = "kituz.html"
    context = {
        'temak': Temakor.objects.all().order_by('sorrend'),
        'szam' : request.user.git.mibol_mennyi(),
        'csoportok': Group.objects.all(),
        'APP_URL_LABEL' : APP_URL_LABEL,
        }
    return render(request, template, context)

@user_passes_test(lambda user : tagja(user, 'adminisztrator'))
def adminisztracio(request:HttpRequest) -> HttpResponse:
    template = "adminisztracio.html"
    context = {
        'csoportok': Group.objects.all(),
        'szam' : request.user.git.mibol_mennyi(),
        'APP_URL_LABEL' : APP_URL_LABEL,
        }
    return render(request, template, context)

@user_passes_test(lambda user : tagja(user, 'tanar'))
def ellenorzes_csoportvalasztas(request:HttpRequest) -> HttpResponse:
    template = "ellenorzes_csoportvalasztas.html"
    csoportok = sorted([t.csoport for t in Tanit.objects.filter(tanar = request.user)], key=lambda l: l.name)
    context = {
        'csoportok': csoportok,
        'szam' : request.user.git.mibol_mennyi(),
        'APP_URL_LABEL' : APP_URL_LABEL,
        }
    return render(request, template, context)

def aktualis_tanev_eleje():
    most = timezone.now()
    tipp = timezone.make_aware(datetime(most.year, 9, 1), timezone=pytz.timezone("Europe/Budapest"))
    if most < tipp:
        return timezone.make_aware(datetime(most.year-1, 9, 1), timezone=pytz.timezone("Europe/Budapest"))
    return tipp

@user_passes_test(lambda user : tagja(user, 'tanar'))
def ellenorzes(request:HttpRequest, csoport:str) -> HttpResponse:
    a_group = Group.objects.filter(name=csoport).first()
    if a_group==None:
        return HttpResponse('ilyen csoport nincs')
    a_userek = User.objects.filter(groups__name=a_group.name)#.order_by('last_name', 'first_name')
    ettol = aktualis_tanev_eleje()
    a_csoport_kituzesei = list(filter(lambda k: ettol <= k.ido, Kituzes.objects.filter(group=a_group)))
    
    
    # mehetne modellbe!
    userek_sorai = []
    for a_user in a_userek:
        a_user_hazifeladatai = []
        for a_kituzes in a_csoport_kituzesei:
            a_hf = Hf.objects.filter(user=a_user, kituzes=a_kituzes).first()
            a_user_hazifeladatai.append(a_hf if a_hf != None else {'na':'valami'} )
            
        userek_sorai.append({
            'user': a_user,
            'hazifeladatai': a_user_hazifeladatai,
            'mentorai': [mentor for mentor in Mentoral.oi(a_user) if not mentor.git.tanar()],
            })
    
    # mehetne modellbe idáig!
    
    
    template = "ellenorzes.html"
    
    
    context = {
        'kituzesek_szama': len(a_csoport_kituzesei),
        'kituzesek': a_csoport_kituzesei,
        'userek': a_userek,
        'userek_sorai': userek_sorai,
        'szam' : request.user.git.mibol_mennyi(),
        'APP_URL_LABEL' : APP_URL_LABEL,
        }
    return render(request, template, context)
