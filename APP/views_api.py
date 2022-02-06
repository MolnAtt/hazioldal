from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Repo

@api_view(['GET'])
def get_repo(request, repoid):
    a_repo = Repo.objects.filter(id=repoid).first()
    if a_repo == None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response({'repo_url': a_repo.url})

@api_view(['POST'])
def update_repo(request, repoid):
    a_repo = Repo.objects.filter(id=repoid).first()
    if a_repo == None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    a_repo.url = request.data['repo_url']
    a_repo.save()
    return Response(f'a {repoid} id-jű repo url-je módosítva erre: {a_repo.url}')

@api_view(['DELETE'])
def delete_repo(request, repoid):
    a_repo = Repo.objects.filter(id=repoid).first()
    if a_repo == None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    a_repo.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
