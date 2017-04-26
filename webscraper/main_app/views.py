from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q  # it's for OR, AND in SQL

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
    if request.method == 'POST':
        tag1 = request.POST.get('tag1')
        tag2 = request.POST.get('tag2')
        tag3 = request.POST.get('tag3')
        source1 = request.POST.get('source1')
        source2 = request.POST.get('source2')

        source1_db = Sources.objects.filter(id=source1).first()  # filter(), instead get(), because of validation
        source2_db = Sources.objects.filter(id=source2).first()  # filter(), instead get(), because of validation
        if source2_db is None or source1_db is None:
            print("Zle zrodla")

        tag1_db = Tags.objects.filter(id=tag1).first()
        tag2_db = Tags.objects.filter(id=tag2).first()
        tag3_db = Tags.objects.filter(id=tag3).first()

        found_articles = Articles.objects\
                    .filter(Q(sourceID=source1_db) | Q(sourceID=source2_db))\
                    .filter(Q(articletagmap__tagID=tag1_db)
                            & Q(articletagmap__tagID=tag2_db)
                            & Q(articletagmap__tagID=tag3_db))\
                    .distinct()
        print(found_articles)

        sources = Sources.objects.order_by('name')
        tags = Tags.objects.order_by('name')

        data = {
            "sources": sources,
            "tags": tags,
            "articles": found_articles
        }
        return render(request, 'main_app/Board.html', data)
    else:
        sources = Sources.objects.order_by('name')
        tags = Tags.objects.order_by('name')

        data = {
            "sources": sources,
            "tags": tags,
        }
    return render(request, 'main_app/Board.html', data)

@login_required
def profile(request):
    return render(request, 'main_app/Profile.html')