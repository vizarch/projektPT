from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *

def start_page(request):
        return render(request, 'main_app/Home.html')

def sources_and_tags(request):
    all_sources = Sources.objects.all()
    all_tags = Tags.objects.all()
    data = {
        "sources": all_sources,
        "tags": all_tags
    }
    return render(request, 'main_app/Sources_and_Tags.html', data)

@login_required
def board(request):
    return render(request, 'main_app/Board.html')

@login_required
def profile(request):
    return render(request, 'main_app/Profile.html')