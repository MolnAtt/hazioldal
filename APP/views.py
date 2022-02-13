from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse, response
from .models import Hf, Mentoral, Mo, Biralat

@login_required
def index(request: HttpRequest) -> HttpResponse:
    return redirect(f'http://{request.get_host()}/attekintes/hf/fontos/')


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

    print(Hf.objects.get(id=2).allapot())

    return render(request, "hazik.html", { 
        'hazik': Hf.lista_to_template(hazik),
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




    """
    lehetséges értékei:
    - NINCS_REPO: a mentorált még nem változtatta meg a default repo linket azaz a https://github.com/ -ot.
    - NINCS_MO: a mentoráltnak már van repo-ja, de még nem nyújtott be megoldást rá.
    - NINCS_BIRALAT: a mentoráltnak már van repoja, van utolsó megoldása, amire viszont még nem kapott bírálatot.
    - VAN_NEGATIV_BIRALAT: a mentoráltnak már van repoja, van utolsó megoldása és ennek van bírálata is: ezek közt viszont van egy negatív.
    - MINDEN_BIRALAT_POZITIV: a mentoráltnak már van repoja, van utolsó megoldása és ennek minden bírálata pozitív.
    """