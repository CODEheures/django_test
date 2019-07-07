# from django.shortcuts import render
from django.http import HttpResponse
from .models import Album, Artist, Contact, Booking
# Create your views here.


def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:4]
    formated_albums = ["<li><a href='/store/album/{}'>{}</a></li>"
                           .format(album.id, album.title) for album in albums]
    message = "<ul>{}</ul>".format("\n".join(formated_albums))

    return HttpResponse(message)


def listing(request):
    albums = Album.objects.filter(available=True)
    formated_albums = ["<li><a href='/store/album/{}'>{}</a></li>"
              .format(album.id, album.title) for album in albums]
    message = "<ul>{}</ul>".format("\n".join(formated_albums))

    return HttpResponse(message)


def detail(request, album_id):
    album = Album.objects.get(pk=int(album_id))
    artists = " ".join(artist.name for artist in album.artists.all())
    message = "Le nom de l'album est {}. Il a été écrit par {}".format(album.title, artists)
    return HttpResponse(message)

def search(request):
    query = request.GET['query']
    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)

    if not albums.exists():
        albums = Album.objects.filter(artists__name__icontains=query)

    if not albums.exists():
        message = "Aucun album ne correspond à votre recherche"
    else:
        liste_html = ["<li>{}</li>".format(album.title) for album in albums]
        message = "Votre recherche: <ul>{}</ul>".format("\n".join(liste_html))

    return HttpResponse(message)
