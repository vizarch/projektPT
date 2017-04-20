from django.shortcuts import render

def start_page(request):
    if request.user.is_authenticated:
        # jest zalogowany
        return render(request, 'main_app/Home_4_logged.html')
    else:
        # NIE jest zalogowany
        return render(request, 'main_app/Home_4_notLogged.html')