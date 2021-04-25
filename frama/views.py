from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.http import Http404

from .models import File


# Create your views here.

def index(request):
    return HttpResponse("In index!")


def files_view(request):
    files = File.objects.all()
    print(files)
    return HttpResponse(str(files))


def add_file(request):
    if request.method == "GET":
        return render(request, "frama/addFile.html", {"title": "Eluińsko"})
    elif request.method == "POST":
        fname: str = request.POST["fname"]
        lname: str = request.POST["lname"]

        print(f"Tried with {fname} {lname}")
        return HttpResponse(f"Tried with {fname} {lname}")
    else:
        raise Http404("add_file")
