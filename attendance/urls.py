from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'list/',
        views.attendance_list,
        name='attendance_list'
    ),

]