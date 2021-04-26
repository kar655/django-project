from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django import forms

from .models import File, User, Directory
from .forms import FileForm, UserForm, DirectoryForm


def index(request):
    request.session["uname_id"] = 1
    print(request.session["uname_id"])
    return HttpResponse("In index!", request)


def files_view(request):
    files = File.objects.all()
    print(files)
    return HttpResponse(str(files))


# def add_file(request):
#     # if request.method == "GET":
#     #     return render(request, "frama/addFile.html", {"title": "Eluińsko"})
#     # elif request.method == "POST":
#     #     fname: str = request.POST["fname"]
#     #     lname: str = request.POST["lname"]
#     #
#     #     print(f"Tried with {fname} {lname}")
#     #     return HttpResponse(f"Tried with {fname} {lname}")
#     # else:
#     #     raise Http404("add_file")
#     form = FileForm(request.POST)
#
#     if form.is_valid():
#         form.save()


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("index")


class DirectoryCreateView(CreateView):
    model = Directory
    form_class = DirectoryForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = User.objects.get(pk=self.request.session["uname_id"])
        form.instance.user = user
        return super(DirectoryCreateView, self).form_valid(form)


class FileCreateView(CreateView):
    model = File
    form_class = FileForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = User.objects.get(pk=self.request.session["uname_id"])
        form.instance.user = user
        return super(FileCreateView, self).form_valid(form)


def tree(request):
    root_directory = Directory.objects.get(pk="ROOT")  # TODO
    return render(request, "frama/directory_tree.html", {
        "recursive_structure": [root_directory]
    })


def tree_highlight(request, chosen_file):
    file = get_object_or_404(File, pk=chosen_file)

    root_directory = Directory.objects.get(pk="ROOT")
    return render(request, "frama/directory_tree.html", {
        "recursive_structure": [root_directory],
        "chosen_file": file
    })
