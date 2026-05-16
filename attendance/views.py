from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from students.models import Student

from .models import Attendance

from datetime import datetime
from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Attendance

from .serializers import AttendanceSerializer


# DASHBOARD
@login_required(login_url='/accounts/login/')
def dashboard(request):

    total_students = Student.objects.count()

    present_count = Attendance.objects.filter(
        status='Present'
    ).count()

    absent_count = Attendance.objects.filter(
        status='Absent'
    ).count()

    total_attendance = Attendance.objects.count()

    attendance_percentage = 0

    if total_attendance > 0:

        attendance_percentage = (
            present_count / total_attendance
        ) * 100

    context = {

        'total_students': total_students,

        'present_count': present_count,

        'absent_count': absent_count,

        'total_attendance': total_attendance,

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


# ATTENDANCE LIST
@login_required(login_url='/accounts/login/')
def attendance_list(request):

    students = Student.objects.all()

    # SELECT DATE

    selected_date = request.GET.get('date')

    if not selected_date:

        selected_date = datetime.today().strftime('%Y-%m-%d')

    attendance_date = datetime.strptime(
        selected_date,
        '%Y-%m-%d'
    ).date()

    # SAVE ATTENDANCE

    if request.method == 'POST':

        selected_date = request.POST.get('date')

        attendance_date = datetime.strptime(
            selected_date,
            '%Y-%m-%d'
        ).date()

        for student in students:

            status = request.POST.get(
                f'status_{student.id}'
            )

            # CHECKBOX LOGIC

            if status == 'on':

                status = 'Present'

            else:

                status = 'Absent'

            Attendance.objects.update_or_create(

                student=student,

                date=attendance_date,

                defaults={

                    'status': status

                }

            )

        return redirect(
            f'/attendance/list/?date={selected_date}'
        )

    # LOAD ATTENDANCE

    attendance_data = []

    for student in students:

        attendance = Attendance.objects.filter(

            student=student,

            date=attendance_date

        ).first()

        attendance_data.append({

            'student': student,

            'status': attendance.status if attendance else ''

        })

    context = {

        'attendance_data': attendance_data,

        'selected_date': selected_date

    }

    return render(
        request,
        'attendance/attendance_list.html',
        context
    )



# LIST + CREATE
class AttendanceListCreateAPI(APIView):

    def get(self, request):

        attendance = Attendance.objects.all()

        serializer = AttendanceSerializer(
            attendance,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = AttendanceSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# RETRIEVE + UPDATE + DELETE
class AttendanceRetrieveUpdateDeleteAPI(APIView):

    def get(self, request, pk):

        attendance = get_object_or_404(
            Attendance,
            pk=pk
        )

        serializer = AttendanceSerializer(
            attendance
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


    def patch(self, request, pk):

        attendance = get_object_or_404(
            Attendance,
            pk=pk
        )

        serializer = AttendanceSerializer(

            attendance,

            data=request.data,

            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    def delete(self, request, pk):

        attendance = get_object_or_404(
            Attendance,
            pk=pk
        )

        attendance.delete()

        return Response(

            {
                'message':
                'Attendance deleted successfully'
            },

            status=status.HTTP_200_OK
        )