from django.test import TestCase
from django.urls import reverse

from .models import Album, Artist, Contact, Booking

# Create your tests here.

#Index page
class IndexPageTestCase(TestCase):

    def setUp(self) -> None:
        self.album = Album.objects.create(title="Mon bel album")
        self.album_id = Album.objects.get(title="Mon bel album").id

    # test status 200
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

#Detail page
    # test return 200 if item exists
    def test_detail_page_return_200(self):
        response = self.client.get(reverse('store:detail', args=[self.album_id]))
        self.assertEqual(response.status_code, 200)

    # test return 404 if not exists
    def test_detail_page_return_404(self):
        response = self.client.get(reverse('store:detail', args=[self.album_id+1]))
        self.assertEqual(response.status_code, 404)

# Booking page
class BookingPageTestCase(TestCase):

    def setUp(self) -> None:
        self.contact = Contact.objects.create(name="Freddie", email="fred@queens.com")
        self.album = Album.objects.create(title="Mon bel album")
        self.artist = Artist.objects.create(name="hot")
        self.album.artists.add(self.artist)

    # Test new booking made
    def test_booking_new_is_registered(self):
        old_bookings = Booking.objects.count()
        response = self.client.post(reverse('store:detail', args=[self.album.id]),
                                    {'name': self.contact.name, 'email': self.contact.email})
        new_bookings = Booking.objects.count()
        self.assertEqual(new_bookings - old_bookings, 1)
    # Test contact on booking
    def test_contact_on_booking(self):
        response = self.client.post(reverse('store:detail', args=[self.album.id]),
                                    {'name': self.contact.name, 'email': self.contact.email})
        last_bookings = Booking.objects.get(album=self.album)
        self.assertEqual(last_bookings.contact.name, self.contact.name)
    # Test album on booking
    def test_album_on_booking(self):
        response = self.client.post(reverse('store:detail', args=[self.album.id]),
                                    {'name': self.contact.name, 'email': self.contact.email})
        last_bookings = Booking.objects.filter(album=self.album)
        self.assertEqual(last_bookings.count(), 1)
    # Test not available album after booking
    def test_album_not_available_after_booking(self):
        response = self.client.post(reverse('store:detail', args=[self.album.id]),
                                    {'name': self.contact.name, 'email': self.contact.email})
        self.album.refresh_from_db()
        self.assertFalse(self.album.available)