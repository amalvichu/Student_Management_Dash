from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, Achievement
from .forms import StudentForm, AchievementForm
import json
from django.db.models import Count, Q

@login_required
def dashboard(request):
    # ALWAYS get all students so stats and graphs stay full/consistent
    students = Student.objects.all()
    
    total_students = students.count()
    approved_achievements = Achievement.objects.filter(status='Approved').count()

    # Chart Data (Always calculated from the FULL dataset)
    dept_data_qs = Student.objects.values('department').annotate(count=Count('id'))
    dept_labels = json.dumps([d['department'] for d in dept_data_qs])
    dept_counts = json.dumps([d['count'] for d in dept_data_qs])

    status_data_qs = Achievement.objects.values('status').annotate(count=Count('id'))
    status_labels = json.dumps([s['status'] for s in status_data_qs])
    status_counts = json.dumps([s['count'] for s in status_data_qs])

    return render(request, 'Student/dashboard.html', {
        'students': students, 
        'total_students': total_students,
        'approved_achievements': approved_achievements,
        'dept_labels': dept_labels,
        'dept_counts': dept_counts,
        'status_labels': status_labels,
        'status_counts': status_counts,
    })

@login_required
def student_list(request):
    query = request.GET.get('q', '')
    if query:
        students = Student.objects.filter(register_number__icontains=query)
    else:
        students = Student.objects.all() # [cite: 35]
    return render(request, 'Student/student_list.html', {'students': students, 'query': query})

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    # --- NEW: Chart Data for Individual Student ---
    ach_stats = student.achievements.values('status').annotate(count=Count('id'))
    s_labels = json.dumps([a['status'] for a in ach_stats])
    s_counts = json.dumps([a['count'] for a in ach_stats])
    
    return render(request, 'Student/student_detail.html', {
        'student': student,
        's_labels': s_labels,
        's_counts': s_counts,
        'total_achievements': student.achievements.count()
    })

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save() # [cite: 34]
            return redirect('dashboard')
    else:
        form = StudentForm()
    return render(request, 'Student/generic_form.html', {'form': form, 'title': 'Add Student'})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save() # [cite: 37]
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'Student/generic_form.html', {'form': form, 'title': f'Edit {student.name}'})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete() # [cite: 38]
        return redirect('dashboard')
    return render(request, 'Student/generic_form.html', {'title': f'Delete {student.name}?', 'is_delete': True})

@login_required
def achievement_create(request):
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES)
        if form.is_valid():
            achievement = form.save() # [cite: 39]
            return redirect('student_detail', pk=achievement.student.pk)
    else:
        form = AchievementForm()
    return render(request, 'Student/generic_form.html', {'form': form, 'title': 'Add Achievement'})

@login_required
def achievement_update(request, pk):
    achievement = get_object_or_404(Achievement, pk=pk)
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES, instance=achievement)
        if form.is_valid():
            form.save() # [cite: 41]
            return redirect('student_detail', pk=achievement.student.pk)
    else:
        form = AchievementForm(instance=achievement)
    return render(request, 'Student/generic_form.html', {'form': form, 'title': 'Edit Achievement'})

@login_required
def achievement_delete(request, pk):
    achievement = get_object_or_404(Achievement, pk=pk)
    student_pk = achievement.student.pk
    if request.method == 'POST':
        achievement.delete() # [cite: 42]
        return redirect('student_detail', pk=student_pk)
    return render(request, 'Student/generic_form.html', {'title': f'Delete {achievement.title}?', 'is_delete': True})

@login_required
def update_achievement_status(request, pk, status):
    achievement = get_object_or_404(Achievement, pk=pk)
    if status in ['Approved', 'Rejected', 'Pending']:
        achievement.status = status # [cite: 43]
        achievement.save()
    return redirect('student_detail', pk=achievement.student.pk)