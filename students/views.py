from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

# Student List
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

# Add Student
def add_student(request):
    form = StudentForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('student_list')

    return render(request, 'students/add_student.html', {'form': form})

# Update Student
def update_student(request, id):

    student = get_object_or_404(Student, id=id)

    form = StudentForm(request.POST or None, instance=student)

    if form.is_valid():
        form.save()
        return redirect('student_list')

    return render(request, 'students/update_student.html', {'form': form})

# Delete Student
def delete_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()
        return redirect('student_list')

    return render(request, 'students/delete_student.html', {'student': student})

# View Student Details
def view_student(request, id):

    student = get_object_or_404(Student, id=id)

    return render(
        request,
        'students/view_student.html',
        {'student': student}
    )