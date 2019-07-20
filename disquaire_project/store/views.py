from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Album, Artist, Contact, Booking
from .forms import ContactForm
# Create your views here.


def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:6]
    context = {'albums': albums}
    return render(request, 'store/index.html', context)


def listing(request):
    albums_list = Album.objects.filter(available=True)
    paginator = Paginator(albums_list, 3)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)

    context = {
        'albums': albums,
        'paginate': True
    }
    return render(request, 'store/listing.html', context)


def detail(request, album_id):
    album = get_object_or_404(Album, pk=int(album_id))
    artists_name = " ".join(artist.name for artist in album.artists.all())
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'album_available': album.available,
        'thumbnail': album.picture
    }

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            contact = Contact.objects.filter(email=email)
            if not contact.exists():
                contact = Contact.objects.create(
                    email = email,
                    name = name
                )
            else:
                contact = contact[0]
            booking = Booking.objects.create(
                album = album,
                contact = contact
            )

            album.available = False
            album.save()
            context = {
                'album_title': album.title
            }
            return render(request, 'store/merci.html', context)
        else:
            context['errors'] = form.errors.items()
    else:
        form = ContactForm()


    context['form'] = form
    return render(request, 'store/detail.html', context)

def search(request):
    query = request.GET['query']
    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)

    if not albums.exists():
        albums = Album.objects.filter(artists__name__icontains=query)

    title = "Résultats pour la requête {}".format(query)
    context = {
        'title': title,
        'albums': albums
    }
    return render(request, 'store/search.html', context)
