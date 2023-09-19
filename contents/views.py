from django.shortcuts import render

# Create your views here.
def contents(request):
    return render(request, "contents/contents.html")