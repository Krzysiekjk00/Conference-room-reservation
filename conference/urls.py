"""conference URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from reservation.views import Show_all, New_room, Modify_room, Delete_room, Room_details, New_reservation, Search_room


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rooms/all/$', Show_all.as_view(), name='all_rooms'),
    url(r'^rooms/new/$', New_room.as_view(), name='new_room'),
    url(r'^rooms/modify/(?P<id>(\d)+)$', Modify_room.as_view(), name='modify_room'),
    url(r'^rooms/delete/(?P<room_id>(\d)+)$', Delete_room.as_view(), name='delete_room'),
    url(r'^rooms/(?P<room_id>(\d)+)$', Room_details.as_view(), name='room_details'),
    url(r'^rooms/reservation/(?P<room_id>(\d)+)$', New_reservation.as_view(), name='new_reservation'),
    url(r'^rooms/search/$', Search_room.as_view(), name='search_room'),
]
