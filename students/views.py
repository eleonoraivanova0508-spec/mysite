from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import UserProfileForm, ProfileForm, GradeForm, RegisterForm
from django.db.models import Avg
from .models import Student, Grade, Group, Club
from .models import Profile

# ГЛАВНАЯ СТРАНИЦА
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/index.html', {
        'students': students
    })

# ПРОФИЛЬ - РЕДАКТИРОВАНИЕ
@login_required
def profile_edit(request):
    # гарантируем, что профиль есть
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('profile_edit')
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'students/profile_edit.html', context)

# СМЕНА ПАРОЛЯ
@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменён!')
            return redirect('profile_edit')
        else:
            print(form.errors)  # 👈 смотри в консоли
            messages.error(request, 'Ошибка при смене пароля')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'students/password_change.html', {'form': form})
# ДОБАВЛЕНИЕ СТУДЕНТА
@login_required
def add_student(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        club_id = request.POST.get("club")
        photo = request.FILES.get("photo")

        club = None
        if club_id:
            club = Club.objects.get(id=club_id)

        Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            club=club,
            photo=photo
        )
        return redirect('student_list')

    return render(request, 'students/add_student.html')

# ДЕТАЛЬНАЯ ИНФОРМАЦИЯ
@login_required
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'students/detail.html', {'student': student})

# РЕДАКТИРОВАНИЕ
@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.age = request.POST.get("age")
        student.phone = request.POST.get("phone")
        student.email = request.POST.get("email")

        # ГРУППА
        group_id = request.POST.get("group")
        if group_id:
            student.group = Group.objects.get(id=group_id)
        else:
            student.group = None

        # КЛУБ
        club_id = request.POST.get("club")
        if club_id:
            student.club = Club.objects.get(id=club_id)
        else:
            student.club = None

        if "photo" in request.FILES:
            student.photo = request.FILES["photo"]

        student.save()
        return redirect('student_list')

    return render(request, "students/edit_student.html", {
        "student": student,
        "groups": Group.objects.all(),
        "clubs": Club.objects.all()
    })

# УДАЛЕНИЕ
@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('student_list')

# СТАТИСТИКА СТУДЕНТА
@login_required
def student_statistics(request, id):
    student = get_object_or_404(Student, id=id)
    grades = Grade.objects.filter(student=student)
    return render(request, 'students/statistics.html', {
        'student': student,
        'grades': grades
    })

# ДОБАВЛЕНИЕ ОЦЕНКИ
@login_required
def add_grade(request):
    students = Student.objects.all()

    if request.method == "POST":
        student_id = request.POST.get('student')
        subject = request.POST.get('subject')
        score = request.POST.get('score')
        comment = request.POST.get('homework_comment')

        student = get_object_or_404(Student, id=student_id)

        Grade.objects.create(
            student=student,
            subject=subject,
            score=score,
            homework_comment=comment
        )
        return redirect('student_list')

    return render(request, 'add_grade.html', {
        'students': students
    })

# ОБЩАЯ СТАТИСТИКА
@login_required
def overall_stats(request):
    grades = Grade.objects.all()
    avg_score = grades.aggregate(Avg('score'))['score__avg']
    return render(request, 'students/overalla_stats.html', {
        'grades': grades,
        'avg_score': avg_score
    })

# РЕГИСТРАЦИЯ
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )

            # 👇 создаём профиль сразу
            Profile.objects.create(user=user)

            messages.success(request, 'Регистрация успешна! Теперь войдите в систему.')
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "students/register.html", {
        "form": form
    })

# ЛОГИН
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('student_list')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    
    return render(request, 'students/login.html')