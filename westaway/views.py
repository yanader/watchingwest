from django.shortcuts import render, redirect, HttpResponse
import csv
from .models import Opponent, Entry, Image, PasswordEntry
from .forms import EntryUploadForm

# Create your views here.

def index(request):
    entries = Entry.objects.all().order_by('-date')
    context = {
        'entries' : entries
    }
    return render(request,"westaway/index.html", context)


def crop(request):
    entry = Entry.objects.first()
    img = entry.image.photo

    return render(request, "westaway/crop.html", {
        "img":img
    })


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


def image(request, filename):
    entry = Entry.objects.first()
    return entry.photo

def entry(request, id):
    entry = Entry.objects.get(id=id)
    return render(request, "westaway/entry.html", {
        "entry": entry
    })