from django.db import models

from datetime import date

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=64)
    num_of_seats = models.IntegerField()
    is_beamer = models.BooleanField(default=False)

    def is_currently_booked(self):
        bookings_today = self.reservations.filter(date=date.today())
        return len(bookings_today) != 0

    # def is_booked_on(self, date):
    #     booked_on = self.reservations.get

class Reservation(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Room, related_name='reservations')
    person = models.CharField(max_length=64)
    comment = models.TextField(default='', blank=True)

    class Meta:
        # Zapewniamy, że na dany dzień dla sali jest tylko jedna rezerwacja
        unique_together = ('room', 'date')