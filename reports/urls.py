from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.report_dashboard,
        name='report_dashboard'
    ),

    path(
        'low-attendance/',
        views.low_attendance,
        name='low_attendance'
    ),

    path(
        'monthly-report/',
        views.monthly_report,
        name='monthly_report'
    ),

    path(
        'student-report/',
        views.student_report,
        name='student_report'
    ),

    path(
        'date-range-report/',
        views.date_range_report,
        name='date_range_report'
    ),

    path(
        'export-pdf/',
        views.export_pdf,
        name='export_pdf'
    ),

]