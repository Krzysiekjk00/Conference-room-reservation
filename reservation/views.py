import datetime

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, render_to_response, redirect
from django.utils.dateparse import parse_date
from django.views import View
from reservation.models import Room, Reservation
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError

# Create your views here.

class Show_all(View):

    def get(self, request):
        rooms = Room.objects.all()
        current_date = str(datetime.date.today())
        search_button = request.GET.get('search')
        if search_button:
            name = request.GET.get('room_name')
            min_num_of_seats = request.GET.get('num_of_seats')
            if request.GET.get('beamer') == 'yes':
                is_beamer = True
            else:
                is_beamer = False
            date = request.GET.get('date')
            return redirect('/rooms/search/?name={}&num_of_seats={}&beamer={}&date={}'.format(name, min_num_of_seats,
                                                                                         is_beamer, date))
        return render_to_response('all_rooms.html', {
            'all_rooms': rooms,
            'current_date': current_date,
        })

class Search_room(View):

    def get(self, request):
        # import pdb
        # pdb.set_trace()
        room_name = request.GET.get('name')
        if request.GET.get('num_of_seats'):
            num_of_seats = request.GET.get('num_of_seats')
        else:
            num_of_seats = 2
        if request.GET.get('beamer') == 'True':
            beamer = True
        else:
            beamer = False
        date = parse_date(request.GET.get('date'))
        bookings = Reservation.objects.filter(date=date)
        reservation_list = [booking.room_id for booking in bookings]
        rooms_available = Room.objects.filter(name__contains=room_name, num_of_seats__gte=num_of_seats,
                                              is_beamer=beamer).exclude(id__in=reservation_list)
        return render(request, 'search_room.html', {
            'rooms': rooms_available,
        })

class New_room(View):

    def get(self, request):
        return render(request, 'new_room.html')

    def post(self, request):
        new_name = request.POST.get('room_name')
        num_of_seats = request.POST.get('seat_nums')
        if request.POST.get('beamer') == 'yes':
            beamer = True
        else:
            beamer = False
        Room.objects.create(name=new_name, num_of_seats=num_of_seats, is_beamer=beamer)
        return HttpResponseRedirect(reverse('all_rooms'))

class Modify_room(View):


    def get(self, request, id):
        room = Room.objects.get(id=id)
        return render(request, 'modify_room.html', {
            'room': room
        })

    def post(self, request, id):
        room = Room.objects.get(id=id)
        edited_name = request.POST.get('edited_name')
        edited_num_of_seats = request.POST.get('edited_seat_nums')
        if request.POST.get('beamer') == 'yes':
            beamer = True
        else:
            beamer = False
        if edited_name:
            room.name = edited_name
        if edited_num_of_seats:
            room.num_of_seats = edited_num_of_seats
        room.is_beamer = beamer
        room.save()
        return HttpResponseRedirect(reverse('all_rooms'))

class Delete_room(View):

    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        return render(request, 'delete_room.html', {
            'room': room,
        })

    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)
        if request.POST.get('yes'):
            room.delete()
        return HttpResponseRedirect(reverse('all_rooms'))

class Room_details(View):

    def get(self, request, room_id):
        current_date = str(datetime.date.today())
        bookings = Reservation.objects.filter(room_id=room_id, date__gte=current_date)
        room = Room.objects.get(id=room_id)
        return render(request, 'room_details.html', {
            'room': room,
            'bookings': bookings,
        })

class New_reservation(View):

    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        current_date = str(datetime.date.today())
        bookings = Reservation.objects.filter(room_id=room_id, date__gte=current_date)
        return render(request, 'new_reservation.html', {
            'room': room,
            'current_date': current_date,
            'bookings': bookings,
        })

    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)
        comment = request.POST.get('comment')
        person = request.POST.get('person')
        try:
            date = parse_date(request.POST['date'])
        except (ValueError, KeyError):
            return HttpResponseBadRequest('Nieprawidlowa data')
        try:
            Reservation.objects.create(room=room, comment=comment, person=person, date=date)
        except IntegrityError:
            return HttpResponseBadRequest('Sala jest zajeta w wybranym terminie')
        return HttpResponseRedirect(reverse('all_rooms')) # ATTRIBUTE ERROR PODCZAS ZAPISYWANIA REZERWACJI 'Reservation' object has no attribute 'get'







