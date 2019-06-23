# from django.shortcuts import render
from django.http import HttpResponse
from .models import ALBUMS
# Create your views here.


def index(request):
    message = "Salut tout le monde!"
    return HttpResponse(message)


def listing(request):
    albums = ["<li><a href='/store/album/{}'>{}</a></li>"
              .format(ind, album['name']) for ind, album in enumerate(ALBUMS)]
    message = "<ul>{}</ul>".format("\n".join(albums))

    return HttpResponse(message)


def detail(request, album_id):
    album = ALBUMS[int(album_id)]
    artists = " ".join(artist['name'] for artist in album['artists'])
    message = "Le nom de l'album est {}. Il a été écrit par {}".format(album['name'], artists)
    return HttpResponse(message)

def search(request):
    query = request.GET['query']
    if not query:
        message = "Faites au moins l'effort de taper une lettre pour la recherche!"
    else:
        albums = [album for album in ALBUMS if query in " ".join(artist['name'] for artist in album['artists'])]

        if len(albums) == 0:
            message = "Aucun album ne correspond à votre recherche"
        else:
            liste_html = ["<li>{}</li>".format(album['name']) for album in albums]
            message = "Votre recherche: <ul>{}</ul>".format("\n".join(liste_html))

    return HttpResponse(message)
