from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django import forms

from .models import File, User, Directory, FileSection
from .forms import FileForm, UserForm, DirectoryForm, FileSectionForm, DirectoryDeleteForm, FileDeleteForm
from .helpers import focus_on_program_elements_helper, get_current_user


def main(request, chosen_file=None):
    request.session["uname_id"] = 1
    file = None
    file_elements = None

    if chosen_file is not None:
        file = get_object_or_404(File, pk=chosen_file, is_valid=True)
        file_elements = focus_on_program_elements_helper(file)

    root_directory = Directory.objects.get(pk="ROOT", is_valid=True)

    return render(request, "frama/index.html", {
        "recursive_structure": [root_directory],
        "chosen_file": file,
        "file_elements": file_elements,
    })


def files_view(request):
    files = File.objects.all()
    print(files)
    return HttpResponse(str(files))


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("main")


class DirectoryCreateView(CreateView):
    model = Directory
    form_class = DirectoryForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        form.instance.user = get_current_user(self.request.session)
        return super(DirectoryCreateView, self).form_valid(form)


class DirectoryDeleteView(FormView):
    template_name = "frama/directory_form.html"
    form_class = DirectoryDeleteForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        directory = form.cleaned_data['directory']
        directory.is_valid = False
        directory.save()
        return super(DirectoryDeleteView, self).form_valid(form)


class FileCreateView(CreateView):
    model = File
    form_class = FileForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        form.instance.user = get_current_user(self.request.session)
        return super(FileCreateView, self).form_valid(form)


class FileDeleteView(FormView):
    template_name = "frama/file_form.html"
    form_class = FileDeleteForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        file = form.cleaned_data['file']
        file.is_valid = False
        file.save()
        return super(FileDeleteView, self).form_valid(form)


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


def focus_on_program_elements(request, chosen_file):
    file = get_object_or_404(File, pk=chosen_file)

    return HttpResponse(focus_on_program_elements_helper(file))


class FileSectionCreateView(CreateView):
    model = FileSection
    form_class = FileSectionForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        form.instance.user = get_current_user(self.request.session)
        return super(FileSectionCreateView, self).form_valid(form)
