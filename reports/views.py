

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from attendance.models import Attendance

# Reports Dashboard
@login_required(login_url='login')
def report_dashboard(request):

    students = Student.objects.all()

    report_data = []

    for student in students:

        total = Attendance.objects.filter(
            student=student
        ).count()

        present = Attendance.objects.filter(
            student=student,
            status='Present'
        ).count()

        percentage = 0

        if total > 0:

            percentage = (
                present / total
            ) * 100

        report_data.append({

            'student': student,

            'total': total,

            'present': present,

            'percentage': round(percentage, 2)

        })

    context = {

        'report_data': report_data

    }

    return render(
        request,
        'reports/report_dashboard.html',
        context
    )

# Low Attendance Report
@login_required(login_url='login')
def low_attendance(request):

    students = Student.objects.all()

    low_students = []

    for student in students:

        total = Attendance.objects.filter(
            student=student
        ).count()

        present = Attendance.objects.filter(
            student=student,
            status='Present'
        ).count()

        percentage = 0

        if total > 0:

            percentage = (
                present / total
            ) * 100

        if percentage < 75:

            low_students.append({

                'student': student,

                'percentage': round(
                    percentage,
                    2
                )

            })

    return render(
        request,
        'reports/low_attendance.html',
        {'low_students': low_students}
    )