from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from attendance.models import Attendance

from django.http import HttpResponse
from reportlab.pdfgen import canvas

# Reports Dashboard
#@login_required(login_url='login')
def report_dashboard(request):

    students = Student.objects.all()

    report_data = []

    for student in students:

        attendance = Attendance.objects.filter(
            student=student
        )

        total = attendance.count()

        present = attendance.filter(
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

            'percentage': round(
                percentage,
                2
            )

        })

    return render(
        request,
        'reports/report_dashboard.html',
        {'report_data': report_data}
    )

# Low Attendance
#@login_required(login_url='login')
def low_attendance(request):

    students = Student.objects.all()

    low_students = []

    for student in students:

        attendance = Attendance.objects.filter(
            student=student
        )

        total = attendance.count()

        present = attendance.filter(
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

# Monthly Report
#@login_required(login_url='login')
def monthly_report(request):

    month = request.GET.get('month')

    attendance = Attendance.objects.all()

    if month:

        attendance = attendance.filter(
            date__month=month
        )

    return render(
        request,
        'reports/monthly_report.html',
        {'attendance': attendance}
    )

# Student Search Report
#@login_required(login_url='login')
def student_report(request):

    query = request.GET.get('q')

    results = []

    if query:

        students = Student.objects.filter(
            name__icontains=query
        )

        for student in students:

            attendance = Attendance.objects.filter(
                student=student
            )

            total = attendance.count()

            present = attendance.filter(
                status='Present'
            ).count()

            percentage = 0

            if total > 0:

                percentage = (
                    present / total
                ) * 100

            results.append({

                'student': student,

                'percentage': round(
                    percentage,
                    2
                )

            })

    return render(
        request,
        'reports/student_report.html',
        {'results': results}
    )
# Date Range Report
#@login_required(login_url='login')
def date_range_report(request):

    attendance = Attendance.objects.all()

    start_date = request.GET.get('start_date')

    end_date = request.GET.get('end_date')

    if start_date and end_date:

        attendance = attendance.filter(
            date__range=[start_date, end_date]
        )

    context = {

        'attendance': attendance

    }

    return render(
        request,
        'reports/date_range_report.html',
        context
    )
# Export PDF
#@login_required(login_url='login')
def export_pdf(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        'attachment; filename="attendance_report.pdf"'
    )

    p = canvas.Canvas(response)

    p.setFont(
        "Helvetica-Bold",
        16
    )

    p.drawString(
        180,
        800,
        "Attendance Report"
    )

    y = 750

    students = Student.objects.all()

    p.setFont(
        "Helvetica",
        12
    )

    for student in students:

        attendance = Attendance.objects.filter(
            student=student
        )

        total = attendance.count()

        present = attendance.filter(
            status='Present'
        ).count()

        percentage = 0

        if total > 0:

            percentage = (
                present / total
            ) * 100

        text = (
            f"{student.name} - "
            f"{round(percentage, 2)}%"
        )

        p.drawString(
            50,
            y,
            text
        )

        y -= 25

    p.save()

    return response