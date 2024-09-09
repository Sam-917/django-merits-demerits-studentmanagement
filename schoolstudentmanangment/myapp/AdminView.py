from django.shortcuts import render, redirect
from .models import MeritStudent, DemeritStudent, Class
from .forms import MeritStudentForm, DemeritStudentForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required


def add_merit_student(request):
    if request.method == 'POST':
        form = MeritStudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_merit_student')
    else:
        form = MeritStudentForm()
    return render(request, 'admin/add-merit-student.html', {'form': form})


def edit_merit_student(request, pk):
    merit_student = MeritStudent.objects.get(pk=pk)
    if request.method == 'POST':
        form = MeritStudentForm(request.POST, instance=merit_student)
        if form.is_valid():
            form.save()
            return redirect('manage_merit_student')
    else:
        form = MeritStudentForm(instance=merit_student)
    return render(request, 'admin/edit-merit-student.html', {'form': form})

def manage_merit_student(request):
    merit_students = MeritStudent.objects.all().order_by('-upload_time')
    return render(request, 'admin/manage-merit-student.html', {'merit_students': merit_students})

def add_demerit_student(request):
    if request.method == 'POST':
        form = DemeritStudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_demerit_student')
    else:
        form = DemeritStudentForm()
    return render(request, 'admin/add-demerit-student.html', {'form': form})

def edit_demerit_student(request, pk):
    demerit_student = DemeritStudent.objects.get(pk=pk)
    if request.method == 'POST':
        form = DemeritStudentForm(request.POST, instance=demerit_student)
        if form.is_valid():
            form.save()
            return redirect('manage_demerit_student')
    else:
        form = DemeritStudentForm(instance=demerit_student)
    return render(request, 'admin/edit-demerit-student.html', {'form': form})

def manage_demerit_student(request):
    demerit_students = DemeritStudent.objects.all().order_by('-upload_time')
    return render(request, 'admin/manage-demerit-student.html', {'demerit_students': demerit_students})

def load_classes(request):
    grade_id = request.GET.get('grade_id')
    classes = Class.objects.filter(grade_id=grade_id).order_by('name')
    class_list = [{'id': c.id, 'name': c.name} for c in classes]
    return JsonResponse(class_list, safe=False)

def delete_merit_student(request, pk):
    merit_student = get_object_or_404(MeritStudent, pk=pk)
    merit_student.delete()
    return redirect('manage_merit_student')

def delete_demerit_student(request, pk):
    demerit_student = get_object_or_404(DemeritStudent, pk=pk)
    demerit_student.delete()
    return redirect('manage_demerit_student')

def tables(request):
    merit_students = MeritStudent.objects.all()
    demerit_students = DemeritStudent.objects.all()
    return render(request, 'admin/tables.html', {'merit_students': merit_students, 'demerit_students': demerit_students})


def charts_view():
    merit_data = MeritStudent.objects.annotate(month=TruncMonth('upload_time')) \
        .values('month') \
        .annotate(count=Count('id')) \
        .order_by('month')

    demerit_data = DemeritStudent.objects.annotate(month=TruncMonth('upload_time')) \
        .values('month') \
        .annotate(count=Count('id')) \
        .order_by('month')

    # Combine the data
    data = {
        'labels': [],
        'merit': [],
        'demerit': []
    }

    for entry in merit_data:
        data['labels'].append(entry['month'].strftime('%B %Y'))
        data['merit'].append(entry['count'])

    for entry in demerit_data:
        if entry['month'].strftime('%B %Y') not in data['labels']:
            data['labels'].append(entry['month'].strftime('%B %Y'))
        data['demerit'].append(entry['count'])

    # Ensure both datasets have the same length
    max_length = max(len(data['merit']), len(data['demerit']))
    data['merit'] += [0] * (max_length - len(data['merit']))
    data['demerit'] += [0] * (max_length - len(data['demerit']))

    return data

@login_required
def dashboard(request):
    if not request.user.is_staff:  # Ensure only admins can access
        return HttpResponse('You are not authorized to view this page.')
    chart_data = charts_view()
    context = {
        'chart_data': chart_data,
        # Add any other data you want to pass to the dashboard
    }
    return render(request, 'admin/index.html', context)
