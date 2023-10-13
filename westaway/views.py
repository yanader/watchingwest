import random
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models.functions import Coalesce
from .models import Opponent, Entry, PasswordEntry
from .forms import EntryUploadForm

# Create your views here.

def index(request):
    entries = Entry.objects.all().order_by('-date')
    context = {
        'entries' : entries
    }
    return render(request,"westaway/index.html", context)


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
    return render(request, "westaway/create.html", {'form':form})


def entry(request, id):
    entry = Entry.objects.get(id=id)
    return render(request, "westaway/entry.html", {
        "entry": entry
    })


def mostvisited(request):
    league = Opponent.objects.annotate(entry_count=Count('entry')).filter(entry_count__gt=0).order_by('-entry_count')
    for team in league:
        print(team.name + ' ' + str(team.entry_count))
    return render(request, "westaway/mostvisited.html", {
        "league":league
    })

def mostvisited_ajax(request):
    filter_option = request.GET.get('filter_option', 'both')  # Default to 'both' if not provided

    if filter_option == 'both':
        entries = Entry.objects.values('opponent__name').annotate(entry_count=Coalesce(Count('opponent'), 0)).order_by('-entry_count')
    elif filter_option == 'home':
        entries = Entry.objects.filter(home=True).values('opponent__name').annotate(entry_count=Coalesce(Count('opponent'), 0)).order_by('-entry_count')
    elif filter_option == 'away':
        entries = Entry.objects.filter(home=False).values('opponent__name').annotate(entry_count=Coalesce(Count('opponent'), 0)).order_by('-entry_count')
    else:
        return JsonResponse({'error': 'Invalid filter option'})

    data = [{'name': entry['opponent__name'], 'entry_count': entry['entry_count']} for entry in entries]

    return JsonResponse({'data': data})

def randomentry(request):
    ids = Entry.objects.values_list('id', flat=True)
    random_id = random.choice(ids)
    
    entry = Entry.objects.get(id=random_id)
    return render(request, "westaway/entry.html", {
        "entry": entry
    })

def error(request):
    return render(request, "westaway/error.html")