from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout  # for authenticate user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # zarzadzanie uzytkownikami
from django.core.mail import send_mail  # wysylanie maili

from webscraper.settings import EMAIL_HOST_USER  # import maila tej apki
HOST_NAME = "127.0.0.1:8000"  # potrzebne podczas generowanie linku aktywacyjnego przy rejestracji


def login_view(request):
    """
    metoda logowania - po zalogowaniu, udanym lub nie udanym, przekierowywuje do strony glownej, czyli http://127.0.0.1:5000/
    jezeli logowanie bylo udane, pokazuje sie napis "Czy chcesz sie wylogować?
    miejsce przekierowanie ustalone jest w pliku settings.py na samym dole: LOGIN_REDIRECT
    """
    if request.method == "POST":
        username = request.POST.get('username')  # == request.POST['username']
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
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
        # TODO: sprawdzenie emaila
        if User.objects.filter(username=username).exists():
            print("istnieje taki uzytkownik")
            return redirect('main_app:start_page')  # juz taki username istnieje

        new_user = User.objects.create_user(username, email, password, is_active=False)
        new_user.save()

        activation_code = username  # TODO: zrobic generowanie kodu aktywacyjnego
        subject = "Webscraper - Activation Code"
        text = (
            """
            Siemka {},
            \npotwierdz e-mail klikajac w link
            \n{}/activate/{}/
            \nMasters of Masters
            """.format(username, HOST_NAME, activation_code))

        send_mail(
            subject,
            text,
            EMAIL_HOST_USER,
            [email],  # lista adresatow
            fail_silently=False
        )

    return redirect('main_app:start_page')

def activate(request, activation_code):
    user = get_object_or_404(User, username=activation_code)
    user.is_active = True
    user.save()  # django update'uje krotke jak zauwazy ze cos zmieniono
    return redirect('main_app:start_page')