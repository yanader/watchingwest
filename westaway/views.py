import random
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models.functions import Coalesce
from .models import Opponent, Entry, PasswordEntry
from .forms import EntryUploadForm


def index(request):
    entries = Entry.objects.all().order_by('-date')
    return render(request, "westaway/index.html", {'entries': entries})


def create(request):
    if request.method == "POST":
        form = EntryUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST.get('password') != PasswordEntry.objects.first().password:
                return redirect('westaway:error')
            form.save()
            return redirect('westaway:index')
    else:
        form = EntryUploadForm()
    return render(request, "westaway/create.html", {'form': form})


def entry(request, id):
    entry = Entry.objects.get(id=id)
    return render(request, "westaway/entry.html", {'entry': entry})


def mostvisited(request):
    league = (Opponent.objects
              .annotate(entry_count=Count('entry'))
              .filter(entry_count__gt=0)
              .order_by('-entry_count'))
    return render(request, "westaway/mostvisited.html", {'league': league})


def mostvisited_ajax(request):
    filter_option = request.GET.get('filter_option', 'both')

    base_qs = Entry.objects.values('opponent__name').annotate(
        entry_count=Coalesce(Count('opponent'), 0)
    ).order_by('-entry_count')

    if filter_option == 'both':
        entries = base_qs
    elif filter_option == 'home':
        entries = base_qs.filter(home=True)
    elif filter_option == 'away':
        entries = base_qs.filter(home=False)
    else:
        return JsonResponse({'error': 'Invalid filter option'})

    data = [{'name': e['opponent__name'], 'entry_count': e['entry_count']} for e in entries]
    return JsonResponse({'data': data})


def randomentry(request):
    ids = Entry.objects.values_list('id', flat=True)
    entry = Entry.objects.get(id=random.choice(ids))
    return render(request, "westaway/entry.html", {'entry': entry})


def error(request):
    return render(request, "westaway/error.html")