from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q  # it's for OR, AND in SQL
from datetime import datetime
from pytz import timezone  # python timezones
from django.contrib import messages  # TODO

def start_page(request):
        return render(request, 'main_app/Home.html')

def sources_and_tags(request, tag_id=None):
    all_sources = Sources.objects.order_by('name')
    all_tags = Tags.objects.order_by('name')
    data = {
            "sources": all_sources,
            "tags": all_tags,
            "user": request.user
        }

    if tag_id is not None:
        chosen_tag = all_tags.filter(id=tag_id).first()
        linked_articles = Articles.objects.filter(articletagmap__tagID=tag_id)
        if linked_articles is not None:
            data = {
                "sources": all_sources,
                "tags": all_tags,
                "linked_articles": linked_articles,
                "chosen_tag": chosen_tag,
                "user": request.user
            }
    return render(request, 'main_app/Sources_and_Tags.html', data)

@login_required
def board(request):
    if request.method == 'POST' and request.POST.get('tags') != '' and request.POST.get('sources') != '' \
            and request.POST.get('from') != '' and request.POST.get('to') != '':
        tags = request.POST.get('tags').split(",")
        sources = request.POST.get('sources').split(",")
        date_from = request.POST.get('from')
        date_to = request.POST.get('to')

        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        date_from = date_from.replace(tzinfo=timezone('Europe/Warsaw'))
        date_to = datetime.strptime(date_to, '%Y-%m-%d')
        date_to = date_to.replace(tzinfo=timezone('Europe/Warsaw'))

        tags_objects = []
        for tag in tags:
            if tag[0] == " ":
                tag = tag[1:]
            tmp = Tags.objects.filter(name=tag).first()
            if tmp is not None:
                tags_objects.append(tmp.id)

        if "wszystkie" in sources:
            found_articles = Articles.objects\
                .filter(articletagmap__tagID__in=tags_objects)\
                .filter(timestamp__gte=date_from, timestamp__lte=date_to)\
                .distinct().order_by('-timestamp')
        else:
            source_objects = []
            for source in sources:
                if source[0] == " ":
                    source = source[1:]
                tmp = Sources.objects.filter(name=source).first()
                if tmp is not None:
                    source_objects.append(tmp.id)

            found_articles = Articles.objects\
                .filter(sourceID__in=source_objects)\
                .filter(articletagmap__tagID__in=tags_objects) \
                .filter(timestamp__gte=date_from, timestamp__lte=date_to)\
                .distinct().order_by('-timestamp')

        tags_list = [str(tag.name) for tag in Tags.objects.order_by('name')]
        sources_list = [str(source.name) for source in Sources.objects.order_by('name')]
        sources_list.append("wszystkie")

        data = {
            "sources_list": sources_list,
            "tags_list": tags_list,
            "articles": found_articles,
            "query": found_articles.query,
            "chosen_tags": tags,
            "chosen_sources": sources,
            "date_from": date_from,
            "date_to": date_to
        }
        return render(request, 'main_app/Board.html', data)
    else:
        tags_list = [str(tag.name) for tag in Tags.objects.order_by('name')]
        sources_list = [str(source.name) for source in Sources.objects.order_by('name')]
        sources_list.append("wszystkie")

        data = {
            "tags_list": tags_list,
            "sources_list": sources_list
        }
    return render(request, 'main_app/Board.html', data)

@login_required
def profile(request):
    return render(request, 'main_app/Profile.html')