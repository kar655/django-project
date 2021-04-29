from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.http import Http404
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django import forms

from .models import File, User, Directory, FileSection
from .forms import FileForm, UserForm, DirectoryForm, FileSectionForm, DirectoryDeleteForm, FileDeleteForm, \
    TabProversForm, TabVCsForm, ChosenTab
from .helpers import focus_on_program_elements_helper, get_current_user, init_database, read_file


def init(request):
    request.session["uname_id"] = 1
    init_database()
    return HttpResponse("Initialized")


class MainView(TemplateView):
    template_name = "frama/index.html"
    file = None
    file_elements = None
    line_tooltips = None
    file_content = None
    chosen_tab = None
    chosen_tab_name = None
    root_directory = None
    is_result = False

    def print_session(self, request):
        print(f"provers = {request.session.get('provers', None)}")
        print(f"vcs = {request.session.get('vcs', None)}")

    def check_chosen_tab(self):
        if self.chosen_tab is not None and not ChosenTab.has_value(self.chosen_tab):
            raise Http404(f"No tab matches value {self.chosen_tab}")

    def load_chosen_tab(self):
        self.chosen_tab_name = self.chosen_tab
        self.is_result = self.chosen_tab_name == ChosenTab.RESULT
        print(f"chosen_tab_name={self.chosen_tab_name}  is_result={self.is_result}")
        self.chosen_tab = ChosenTab.give_form(self.chosen_tab)

    def load_custom_data(self, chosen_file):
        self.root_directory = Directory.objects.get(pk="ROOT", is_valid=True)

        if chosen_file is not None:
            self.file = get_object_or_404(File, pk=chosen_file, is_valid=True)
            self.file_elements, self.line_tooltips = focus_on_program_elements_helper(self.file)
            self.file_content = read_file(self.file)
        else:
            self.file = None
            self.file_elements = None
            self.line_tooltips = None
            self.file_content = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recursive_structure'] = [self.root_directory]
        context['chosen_file'] = self.file
        context['file_elements'] = self.file_elements
        context['line_tooltips'] = self.line_tooltips
        context['file_content'] = self.file_content
        context['chosen_tab'] = self.chosen_tab
        context['is_result'] = self.is_result

        return context

    def get(self, request, *args, **kwargs):
        self.print_session(request)
        self.chosen_tab = kwargs.get('chosen_tab', None)
        self.check_chosen_tab()
        self.load_chosen_tab()
        self.chosen_tab = self.chosen_tab()

        chosen_file = kwargs.get('chosen_file', None)
        self.load_custom_data(chosen_file)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.chosen_tab = kwargs.get('chosen_tab', None)
        self.check_chosen_tab()
        self.load_chosen_tab()
        self.chosen_tab = self.chosen_tab(request.POST)
        if self.chosen_tab.is_valid():
            request.session[self.chosen_tab_name] = self.chosen_tab.cleaned_data[self.chosen_tab_name]
            print("WORKS ")
            print(f"Got {self.chosen_tab.cleaned_data[self.chosen_tab_name]}")

        chosen_file = kwargs.get('chosen_file', None)
        self.load_custom_data(chosen_file)

        return super().get(request, *args, **kwargs)


def main(request, chosen_tab=None, chosen_file=None):
    request.session["uname_id"] = 1
    file = None
    file_elements = None
    line_tooltips = None
    file_content = None
    chosen_tab_name = chosen_tab

    if chosen_tab is not None and not ChosenTab.has_value(chosen_tab):
        raise Http404(f"No tab matches value {chosen_tab}")

    chosen_tab = ChosenTab.give_form(chosen_tab)(request.POST)

    # testowanie = TabProversForm()
    print(f"In {chosen_tab.is_valid()})")
    # print(f"got {chosen_tab.cleaned_data['vcs']}")

    if chosen_file is not None:
        file = get_object_or_404(File, pk=chosen_file, is_valid=True)
        file_elements, line_tooltips = focus_on_program_elements_helper(file)
        file_content = read_file(file)

    root_directory = Directory.objects.get(pk="ROOT", is_valid=True)

    return render(request, "frama/index.html", {
        "recursive_structure": [root_directory],
        "chosen_file": file,
        "file_elements": file_elements,
        "line_tooltips": line_tooltips,
        "file_content": file_content,
        "chosen_tab": chosen_tab,
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
