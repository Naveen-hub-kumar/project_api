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

      path(

        'api/attendance/',views.

        AttendanceListCreateAPI.as_view(),

        name='attendance_api'

    ),

    path(

        'api/attendance/<int:pk>/',views.

        AttendanceRetrieveUpdateDeleteAPI.as_view(),

        name='attendance_detail_api'

    ),

]