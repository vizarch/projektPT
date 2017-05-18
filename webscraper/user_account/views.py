# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash  # for authenticate user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # zarzadzanie uzytkownikami
from django.core.mail import send_mail  # wysylanie maili
from django.contrib.auth.forms import PasswordChangeForm  # wbudowany formularz zmiany hasla

from django.contrib import messages  # powiadomienia, ktore mozna wyswietlic w HTMLu
import hashlib  # do generowania activation_code

from webscraper.settings import EMAIL_HOST_USER  # import maila tej apki
HOST_NAME = "127.0.0.1:8000"  # potrzebne podczas generowanie linku aktywacyjnego przy rejestracji


def login_view(request):
    """
    metoda logowania
    """
    if request.method == "POST":
        username = request.POST.get('username')  # to samo co request.POST['username']
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        #  sprawdzenie czy haslo pasuje do uzytkownika
        if user is not None:
            login(request, user)
        else:
            messages.error(request, 'Błędny login lub hasło.')
    return redirect('main_app:start_page')  # bez wzgledu na wynik logowania przekirowanie do glownej

@login_required(login_url='/')
def logout_view(request):
    logout(request)
    return redirect('main_app:start_page')

def register_view(request):
    """
    rejestracja uzytkownikow - na adres e-mail wysylany jest link aktywacyjny
    """
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # haslo w bazie zapisywane jest w formacie <algorithm>$<iterations>$<salt>$<hash> i używa PBKDF2
        # https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-PASSWORD_HASHERS

        # sprawdzenie czy uzytkownik o podanym 'username' juz istnieje
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Użytkownik o podanej nazwie już istnieje.')
            return redirect('main_app:start_page')  # juz taki username istnieje

        new_user = User.objects.create_user(username, email, password, is_active=False)
        new_user.save()

        #  generowanie kodu aktywacyjnego: skrot MD5 nazwy uzytkownika+jakis tekst
        activation_code = hashlib.md5(email.encode('utf-8')+b'dUzOSoLi').hexdigest()
        subject = "Webscraper - Activation Code"
        text = (
            """
            Siemka {},
            \npotwierdz e-mail klikajac w link
            \n{}/account/activate/{}/{}/
            \nMasters of Masters
            """.format(username, HOST_NAME, username, activation_code))

        send_mail(subject, text, EMAIL_HOST_USER, [email], fail_silently=False)  # wyslanie maila
        messages.info(request,'Kliknij w link aktywacyjny wysłany na podany adres e-mail.')
    return redirect('main_app:start_page')

def activate(request, username, activation_code):
    """
    metoda do aktywowania konta uzytkownika
    """
    user = get_object_or_404(User, username=username)
    if activation_code == hashlib.md5(user.email.encode('utf-8')+b'dUzOSoLi').hexdigest():
        user.is_active = True
        user.save()  # django domyslnie update'uje krotke, chyba ze wymusimy utworzenie nowej
        logout(request)  # wylogowanie user'a, bo klikniecie w link aktywacyjny od razu go loguje tez
        messages.success(request, 'Aktywacja konta udana.')
    else:
        messages.error(request, 'Aktywacja konta nie udała się. Skontaktuj się z administratorem.')
    return redirect('main_app:start_page')

@login_required(login_url='/')
def user_profile(request):
    """
    metoda wyswietlajaca HTML'a z formularzami do zmiany hasla, maila i usuniecie konta
    """
    return render(request, 'user_account/user_profile.html')

@login_required(login_url='/')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        user = authenticate(username=request.user, password=old_password)
        # sprawdza stare haslo user'a
        # authenticate zwraca obiekt 'User' jesli haslo pasuje do uzytkownika, else zwraca None
        if user is None:
            messages.error(request, 'Podano złe aktualne hasło!')
            return redirect('user_account:user_profile')
        new_pass1 = request.POST.get('new_pass1')
        new_pass2 = request.POST.get('new_pass2')
        if new_pass1 != new_pass2:
            messages.error(request, 'Nowe hasło powtórz dwukrotnie!')
            return redirect('user_account:user_profile')
        user.set_password(new_pass1)
        user.save()
        update_session_auth_hash(request, user)  # aktualizacja biezacej sesji dla user'a z nowym haslem
        messages.success(request, 'Zmiana hasła powiodła się.')
    else:
        messages.error(request, 'Żadne pole hasła nie może być puste!')
    return redirect('user_account:user_profile')

@login_required(login_url='/')
def change_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        obj_user = get_object_or_404(User, username=request.user)
        obj_user.email = new_email
        obj_user.is_active = False  # uzytkownik bedzie musial potwierdzic nowego maila
        obj_user.save()
        username = obj_user.username

        #  to samo co podczas rejestracji: wysyla na maila link aktywacyjny
        activation_code = hashlib.md5(new_email.encode('utf-8') + b'dUzOSoLi').hexdigest()
        subject = "Webscraper - Change email - activation"
        text = (
            """
            Siemka {},
            \npotwierdz e-mail klikajac w link
            \n{}/account/activate/{}/{}/
            \nMasters of Masters
            """.format(username, HOST_NAME, username, activation_code))

        send_mail(subject,text,EMAIL_HOST_USER,[new_email],fail_silently=False)  # wyslanie maila
        logout(request)
        messages.success(request, 'Zmiana adresu e-mail powiodła się.')
        return redirect('main_app:start_page')
    else:
        messages.error(request, 'Adres e-mail nie może być pusty!')
        return redirect('user_account:user_profile')

@login_required(login_url='/')
def account_delete(request):
    user = get_object_or_404(User, username=request.user)
    # user.is_active = False  # TODO: usuwac czy deaktywowac uzytkownika??
    user.delete()  # usuwa uzytkownika i wszystkie dane z nim powiazane
    messages.success(request, 'Usunięto konto.')
    return redirect('main_app:start_page')