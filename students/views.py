from django.shortcuts import render, redirect, get_object_or_404

from .models import Student

from .forms import StudentForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer




# STUDENT LIST
def student_list(request):

    students = Student.objects.all()

    return render(

        request,

        'students/student_list.html',

        {

            'students': students

        }

    )


# ADD STUDENT
def add_student(request):

    form = StudentForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        return redirect('/students/')

    return render(

        request,

        'students/add_student.html',

        {

            'form': form

        }

    )


# VIEW STUDENT
def view_student(request, id):

    student = get_object_or_404( Student, id=id)

    return render( request,'students/view_student.html',

        {

            'student': student

        }

    )


# UPDATE STUDENT
def update_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    form = StudentForm(request.POST or None, instance=student)

    if form.is_valid():

        form.save()

        return redirect('/students/')

    return render( request,'students/update_student.html',

        {

            'form': form

        }

    )


# DELETE STUDENT
def delete_student(request, id):

    student = get_object_or_404( Student,id=id )

    if request.method == 'POST':

        student.delete()

        return redirect('/students/')

    return render(request,'students/delete_student.html',

        {

            'student': student

        }

    )





#API Creation For Student Module
# LIST + CREATE API
class StudentListCreationAPI(APIView):

    def get(self, request):

        students = Student.objects.all()

        serializer = StudentSerializer( students,many=True)

        return Response( serializer.data, status=status.HTTP_200_OK )

    def post(self, request):

        serializer = StudentSerializer(data=request.data )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data,status=status.HTTP_201_CREATED)
            

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST )


# RETRIEVE + UPDATE + DELETE API
class StudentRetrieveUpdateDestroyAPI(APIView):

    # GET SINGLE STUDENT
    def get(self, request, pk):

        student = get_object_or_404( Student,pk=pk)

        serializer = StudentSerializer(student)

        return Response(serializer.data,status=status.HTTP_200_OK )

    # PATCH UPDATE
    def patch(self, request, pk):

        student = get_object_or_404(
            Student,
            pk=pk
        )

        serializer = StudentSerializer(student,data=request.data,partial=True)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data,status=status.HTTP_200_OK )

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST )

    # DELETE STUDENT
    def delete(self, request, pk):

        student = get_object_or_404(Student,pk=pk)

        student.delete()

        return Response(
            {
                'message': 'Student deleted successfully'
            },
            status=status.HTTP_200_OK
        )