from django import forms
from django.contrib.auth.models import User
from bootstrap_datepicker_plus import DatePickerInput


class CreateTaskForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'task-input',
                'placeholder': 'Название',
            }
        )
    )
    comment = forms.CharField(
        max_length=5000,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'large-input task-input',
                'placeholder': 'Комментарий',
            }
        )
    )
    date_start = forms.DateField(
        widget=DatePickerInput(),
        required=True
    )

    date_end = forms.DateField(
        widget=DatePickerInput(),
        required=True
    )

    def valid_date(self):
        cd = self.cleaned_data
        return cd['date_start'] < cd['date_end']


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Логин',
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Пароль',
            }
        )
    )


# New reg form
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
        }
    ))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
        }
    ))

    email = forms.CharField(
        max_length=40,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }
        ))

    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Логин',
            }
        ))

    first_name = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
            }
        ))

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class ChangePassword(forms.Form):
    old_pass = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Старый пароль',
        }
    ))

    new_pass = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Новый пароль',
        }
    ))

    new_pass2 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
        }
    ))


class ChangeName(forms.Form):
    new_name = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'task-input',
                'placeholder': 'Введите новое имя',
            }
        ))

    def name_empty(self):
        cd = self.cleaned_data
        return cd['new_name'] != ''


class ChangeEmail(forms.Form):
    old_email = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Старая почта',
            }
        ))

    new_email = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Новая почта',
            }
        ))

    new_email2 = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Повторите почту',
            }
        ))

    def match_email(self):
        cd = self.cleaned_data
        return cd['new_email'] == cd['new_email2']
