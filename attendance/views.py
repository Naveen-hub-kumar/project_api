from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Attendance
from .forms import AttendanceForm
from students.models import Student

# Dashboard
#@login_required(login_url='login')
def dashboard(request):

    # Total Students
    total_students = Student.objects.count()

    # Total Attendance Records
    total_attendance = Attendance.objects.count()

    # Present Count
    present_count = Attendance.objects.filter(
        status='Present'
    ).count()

    # Absent Count
    absent_count = Attendance.objects.filter(
        status='Absent'
    ).count()

    # Attendance Percentage
    attendance_percentage = 0

    if total_attendance > 0:

        attendance_percentage = (
            present_count / total_attendance
        ) * 100

    # Context
    context = {

        'total_students': total_students,

        'total_attendance': total_attendance,

        'present_count': present_count,

        'absent_count': absent_count,

        'attendance_percentage': round(
            attendance_percentage,
            2
        ),

    }

    return render(
        request,
        'attendance/dashboard.html',
        context
    )

# Attendance List
def attendance_list(request):

    attendance = Attendance.objects.all()

    return render(
        request,
        'attendance/attendance_list.html',
        {'attendance': attendance}
    )

# Mark Attendance
def mark_attendance(request):

    form = AttendanceForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        return redirect(
            'attendance_list'
        )

    return render(
        request,
        'attendance/mark_attendance.html',
        {'form': form}
    )