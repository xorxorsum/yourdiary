import datetime
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from yourdiary.models import Tasks, UserParams
from yourdiary.forms import UserRegistrationForm, LoginForm, CreateTaskForm, ChangePassword, ChangeName, ChangeEmail
from django.contrib import messages
from django.core.files.storage import FileSystemStorage


def get_base_context(request, pagename):
    return {
        'pagename': pagename,
        'username': request.user,
    }


def index_page(request):
    context = get_base_context(request, 'Главная')
    return render(request, 'yourdiary/index.html', context)


def login_page(request):
    context = get_base_context(request, 'Вход')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, "Авторизация успешна")
                    return redirect('index')
                else:
                    messages.add_message(request, messages.ERROR, "Пользователь заблокирован")
            else:
                messages.add_message(request, messages.ERROR, "Неправильный логин или пароль")
        else:
            messages.add_message(request, messages.ERROR, "Некорректные данные в форме авторизации")
    else:
        form = LoginForm()
    context['form'] = form
    return render(request, 'yourdiary/login.html', context)


def logout_page(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Вы успешно вышли из аккаунта")
    return redirect('index')


def register_page(request):
    context = get_base_context(request, 'Регистрация')
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            record = UserParams(
                user=new_user,
                tasks_solved=0,
                tasks_failed=0,
                score=0
            )
            record.save()
            if new_user.is_active:
                login(request, new_user)
                return render(request, 'yourdiary/index.html')
            else:
                messages.add_message(request, messages.ERROR, "Пользователь заблокирован")
        else:
            messages.add_message(request, messages.ERROR, "Некорректные данные в форме авторизации")
    else:
        user_form = UserRegistrationForm()
    context['user_form'] = user_form
    return render(request, 'yourdiary/register.html', context)


def profile_page(request):
    context = get_base_context(request, 'Профиль')
    if request.user.is_authenticated:
        tasks = Tasks.objects.filter(user=request.user)
        current_user = UserParams.objects.get(user=request.user)
        if request.GET.get('id'):
            object = Tasks.objects.get(id=request.GET.get('id'))
            if object.done_indicator == -1:
                current_user.tasks_solved += 1
                current_user.score += 30
                current_user.save()
            object.delete()
        for object in tasks:
            if object.deadline < datetime.date.today() and object.done_indicator!=0:
                object.done_indicator = 0
                object.save()
                current_user.tasks_failed += 1
                current_user.save()
        context['tasks'] = tasks
        context['current_user'] = current_user
    return render(request, 'yourdiary/profile.html', context)


def task_create_page(request):
    context = get_base_context(request, 'Создание задания')
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid() and form.valid_date():
            cd = form.cleaned_data
            record = Tasks(
                user=request.user,
                hostId=cd['date_start'],
                title=cd['title'],
                comment=cd['comment'],
                deadline=cd['date_end']
            )
            record.save()
            return redirect('profile')
        else:
            messages.add_message(request, messages.ERROR, "Некорректные данные в форме")
    else:
        form = CreateTaskForm()
    context['form'] = form
    return render(request, 'yourdiary/task.html', context)


def agreement_page(request):
    context = get_base_context(request, 'Пользовательское соглашение')

    return render(request, 'yourdiary/agreement.html', context)


def settings_page(request):
    context = get_base_context(request, 'Настройки')
    if request.user.is_authenticated:
        current_user = UserParams.objects.get(user=request.user)
        context['current_user'] = current_user
        u = User.objects.get(username=request.user)
        if request.method == 'POST':

            if request.FILES.get('avatarNew'):
                myfile = request.FILES.get('avatarNew')
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                current_user.avatar = fs.url(filename)
                current_user.save()
                messages.add_message(request, messages.SUCCESS, "Вы успешно сменили аватар")

            form = ChangeName(request.POST)
            if form.is_valid():
                if form.name_empty():
                    u.first_name = form.cleaned_data['new_name']
                    u.save()
                    login(request, u)
                    messages.add_message(request, messages.SUCCESS, "Вы успешно сменили имя")
                return redirect('profile')
        else:
            form = ChangeName()
        context['form'] = form
    return render(request, 'yourdiary/settings.html', context)


def change_password(request):
    context = get_base_context(request, 'Смена пароля')
    if request.user.is_authenticated:
        u = User.objects.get(username=request.user)
        if request.method == 'POST':
            form = ChangePassword(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if cd['new_pass']==cd['new_pass2']:
                    new_password = form.cleaned_data['new_pass2']
                    u.set_password(new_password)
                    u.save()
                    login(request, u)
                    messages.add_message(request, messages.SUCCESS, "Вы успешно сменили пароль")
                    return redirect('profile')
        else:
            form = ChangePassword()
        context['form'] = form
    return render(request, 'yourdiary/change_password.html', context)


def change_email(request):
    context = get_base_context(request, 'Смена почты')
    if request.user.is_authenticated:
        u = User.objects.get(username=request.user)
        if request.method == 'POST':
            form = ChangeEmail(request.POST)
            if form.is_valid():
                if form.match_email() and u.email == form.cleaned_data['old_email']:
                    u.email = form.cleaned_data['new_email2']
                    u.save()
                    login(request, u)
                    messages.add_message(request, messages.SUCCESS, "Вы успешно сменили почту")
                    return redirect('profile')
        else:
            form = ChangeEmail()
        context['form'] = form
        return render(request, 'yourdiary/change_email.html', context)


def delete_account(request):
    User.objects.filter(username=request.user).delete()
    UserParams.objects.filter(user=request.user).delete()
    messages.add_message(request, messages.SUCCESS, "Вы успешно удалили аккаунт")
    return redirect('index')

def delete_task(request, id):
    current_user = UserParams.objects.filter(user=request.user)
    Tasks.objects.filter(id=id).delete()
    current_user.tasks_solved += 1
    current_user.score += 30
    current_user.save()
    return redirect('profile')


