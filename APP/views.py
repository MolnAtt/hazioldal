from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse, response
from .serializers import BigyoSerializer
from .models import Bigyo, Hf, Mentoral, Mo, Repo, Biralat

@login_required
def index(request: HttpRequest) -> HttpResponse:
    return redirect(f'http://{request.get_host()}/attekintes/hf/fontos/')


@login_required
def hazik(request: HttpRequest, hfmo: str, szuro: str) -> HttpResponse:
    mentor_vagyok = hfmo == "mo"
    mentoralt_vagyok = hfmo == "hf"
    if hfmo == "mo" and szuro == "osszes":
        hazik = Hf.mentoraltak_hazijainak_unioja(request.user)
    elif hfmo == "mo" and szuro == "fontos":
        hazik = Hf.mentoraltak_hazijainak_unioja(request.user, Hf.a_mentornak_fontos)
    elif hfmo == "hf" and szuro == "osszes":
        hazik = Hf.user_hazijai(request.user)
    elif hfmo == "hf" and szuro == "fontos":
        hazik = Hf.user_hazijai(request.user, Hf.a_mentoraltnak_fontos)
    else:
        hazik = []

    return render(request, "hf.html", { 
        'hazik': Hf.lista_to_template(hazik),
        'mentor_vagyok': mentor_vagyok,
        'mentoralt_vagyok': mentoralt_vagyok,
        })
    

@login_required
def mentoralas(request: HttpRequest, szuro: str) -> HttpResponse:
    mentoraltak_hazijai = []
    for mentorkapcsolat in Mentoral.objects.filter(mentor=request.user):
        mentoraltak_hazijai+= Hf.lista(mentorkapcsolat.mentoree) if szuro =="osszes" else Hf.lista(mentorkapcsolat.mentoree, Hf.a_mentornak_fontos)
    return render(request, "mentoralas.html", { 
        'hazik': mentoraltak_hazijai
    })


@login_required
def repo_create(request:HttpRequest, hfid:int) -> HttpResponse:
    return render(request, "repo_create.html", {        
        'hf': Hf.objects.filter(id=hfid).first()
        })


@login_required
def repo(request:HttpRequest, repoid:int) -> HttpResponse:
    a_repo = Repo.objects.filter(id=repoid).first()
    return render(request, "repo.html", {
        'hf': a_repo.hf,
        'repo': a_repo,
        'mentor_vagyok': a_repo.ban_mentor(request.user),
        'mentoralt_vagyok': a_repo.ban_mentoralt(request.user),
        'uj_megoldast_adhatok_be': a_repo.nak_nincs_megoldasa_vagy_az_utolso_megoldasanak_nincs_biralata_vagy_van_negativ_biralata(),
        'uj_biralatot_rogzithetek': a_repo.nak_van_utolso_megoldasa_es_azt_meg_nem_mentoralta(request.user),
        'megoldasok_es_biralatok': a_repo.megoldasai_es_biralatai(),
    })