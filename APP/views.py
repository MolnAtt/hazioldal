from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse, response
from .serializers import BigyoSerializer
from .models import Bigyo, Hf, Mentoral, Mo, Repo, Biralat

@login_required
def index(request: HttpRequest) -> HttpResponse:
    return redirect(f'http://{request.get_host()}/hf/fontos/')


@login_required
def hazik(request: HttpRequest, szuro: str) -> HttpResponse:
    return render(request, "hf.html", { 
        'hazik': Hf.lista(request.user) if szuro=="osszes" else Hf.lista(request.user, Hf.a_mentoraltnak_fontos)
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
def repo_check(request: HttpRequest, hfid: int) -> HttpResponse:
    a_hf = Hf.objects.filter(id=hfid).first()
    a_repo = Repo.objects.filter(hf=a_hf)
    if a_repo.exists():
        return redirect(f'http://{request.get_host()}/repo/{a_repo.first().id}/')
    else:
        return redirect(f'http://{request.get_host()}/hf/{hfid}/repo/create/')


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
        'uj_megoldast_adhatok_be': a_repo.nak_minden_megoldasa_rossz() or a_repo.nak_van_utolso_megoldasa_es_annak_nincs_biralata(),
        'a_legutolso_megoldasnak_nincs_biralata': a_repo.nak_van_utolso_megoldasa_es_annak_nincs_biralata(),
        'megoldasok_es_biralatok': a_repo.megoldasai_es_biralatai(),
    })