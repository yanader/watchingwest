from django.shortcuts import render, redirect
from django.db.models import Count
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
                return redirect('westaway:index')
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