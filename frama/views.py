from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User

from .forms import FileForm, DirectoryForm, FileSectionForm, DirectoryDeleteForm, FileDeleteForm, \
    ChosenTab, RegisterForm
from .helpers import focus_on_program_elements_helper, read_file, get_result, \
    init_root_directory
from .models import File, Directory, FileSection


class Codemirror(TemplateView):
    template_name = "frama/codemirror.html"


class UserCreateView(CreateView):
    class Meta:
        abstract = True

    def get_form_kwargs(self):
        kwargs = super(UserCreateView, self).get_form_kwargs()
        kwargs.update({'user_id': self.request.user.id})
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserCreateView, self).form_valid(form)


class UserFormView(FormView):
    class Meta:
        abstract = True

    def get_form_kwargs(self):
        kwargs = super(UserFormView, self).get_form_kwargs()
        kwargs.update({'user_id': self.request.user.id})
        return kwargs


class LoginView(auth_views.LoginView):
    template_name = "frama/login_form.html"
    success_url = reverse_lazy("main")
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    template_name = "frama/logout_form.html"
    success_url = reverse_lazy("login")


class RegisterView(CreateView):
    template_name = "frama/login_form.html"
    form_class = RegisterForm
    success_url = reverse_lazy("login")


class ProgramElements(TemplateView):
    template_name = "frama/program_elements.html"

    file = None
    file_elements_sections = None

    def load_custom_data(self, chosen_file, user: User):
        if chosen_file is not None:
            self.file = get_object_or_404(File, name=chosen_file, user=user.id, is_valid=True)
            self.file_elements_sections, _ = focus_on_program_elements_helper(self.file)
        else:
            self.file = None
            self.file_elements_sections = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chosen_file'] = self.file
        context['file_elements_sections'] = self.file_elements_sections
        context['chosen_file_path'] = self.file.file_field.path if self.file else None

        return context

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404()

        chosen_file = request.GET.get('chosen_file', None)
        self.load_custom_data(chosen_file, request.user)

        return super().get(request, *args, **kwargs)


class FileContent(TemplateView):
    template_name = "frama/file_content.html"

    file = None
    file_content = None
    line_tooltips = None

    def load_custom_data(self, chosen_file, user: User):
        if chosen_file is not None:
            self.file = get_object_or_404(File, name=chosen_file, user=user.id, is_valid=True)
            _, self.line_tooltips = focus_on_program_elements_helper(self.file)
            self.file_content = read_file(self.file)
        else:
            self.file = None
            self.line_tooltips = None
            self.file_content = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file_content'] = self.file_content
        context['line_tooltips'] = self.line_tooltips

        return context

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404()

        chosen_file = request.GET.get('chosen_file', None)
        self.load_custom_data(chosen_file, request.user)

        return super().get(request, *args, **kwargs)


class TabsView(TemplateView):
    template_name = "frama/tab_data.html"

    is_chosen_file = True
    chosen_tab = None
    is_result = None
    file = None

    def check_chosen_tab(self):
        if self.chosen_tab is not None and not ChosenTab.has_value(self.chosen_tab):
            raise Http404(f"No tab matches value {self.chosen_tab}")

    def load_chosen_tab(self):
        self.is_result = self.chosen_tab is None or self.chosen_tab == ChosenTab.RESULT
        self.chosen_tab = ChosenTab.give_form(self.chosen_tab)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chosen_file'] = self.file
        context['chosen_tab'] = self.chosen_tab
        context['is_result'] = self.is_result
        context['is_chosen_file'] = self.is_chosen_file

        return context

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404()

        self.chosen_tab = request.GET.get("chosen_tab")
        self.check_chosen_tab()
        self.load_chosen_tab()

        self.file = request.GET.get("chosen_file")

        if self.is_result:
            self.chosen_tab = self.chosen_tab(
                provers=request.session.get('provers', None),
                use_wp_rte=request.session.get('use_wp_rte', None),
                wp_prop_flag=request.session.get('wp_prop_flag', None),
                file_path=self.file if self.file is not None else "no file",
            )
            used_command = f"Results of: {self.chosen_tab}\n\n\n"
            self.chosen_tab = used_command + get_result(self.chosen_tab)
        else:
            self.chosen_tab = self.chosen_tab()

        return super().get(request, *args, **kwargs)


class DirectoryCreateView(UserCreateView):
    model = Directory
    form_class = DirectoryForm
    success_url = reverse_lazy("main")


class DirectoryDeleteView(UserFormView):
    template_name = "frama/directory_delete_form.html"
    form_class = DirectoryDeleteForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        directory = form.cleaned_data['directory']

        def recursively_clear(direc: Directory):
            direc.is_valid = False
            direc.save()

            for file in direc.file_set.all():
                file.is_valid = False
                file.save()

            for child_directory in direc.directory_set.all():
                recursively_clear(child_directory)

        recursively_clear(directory)

        return super(DirectoryDeleteView, self).form_valid(form)


class FileCreateView(UserCreateView):
    model = File
    form_class = FileForm
    success_url = reverse_lazy("main")


class FileDeleteView(UserFormView):
    template_name = "frama/file_delete_form.html"
    form_class = FileDeleteForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        file = form.cleaned_data['file']
        file.is_valid = False
        file.save()
        return super(FileDeleteView, self).form_valid(form)


class FileSectionCreateView(UserCreateView):
    model = FileSection
    form_class = FileSectionForm
    success_url = reverse_lazy("main")


class MainView(TemplateView):
    template_name = "frama/index.html"

    file = None
    root_directory = None

    def load_custom_data(self, chosen_file, user: User):
        self.root_directory = Directory.objects.get(name="ROOT", user=user.id, is_valid=True)

        if chosen_file is not None:
            self.file = get_object_or_404(File, name=chosen_file, user=user.id, is_valid=True)
        else:
            self.file = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recursive_structure'] = [self.root_directory]
        context['chosen_file'] = self.file
        context['chosen_file_path'] = self.file.file_field.path if self.file else None

        return context

    def get(self, request, *args, **kwargs):
        init_root_directory(request.user)
        chosen_file = None
        self.load_custom_data(chosen_file, request.user)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "type" in request.POST:
            request_type = request.POST["type"]
            response = None

            if request_type == "directory_form":
                response = DirectoryCreateView()
            elif request_type == "file_form":
                response = FileCreateView()
            elif request_type == "filesection_form":
                response = FileSectionCreateView()
            elif request_type == "file_delete_form":
                response = FileDeleteView()
            elif request_type == "directory_delete_form":
                response = DirectoryDeleteView()
            else:
                raise Http404("")

            response.request = request
            return response.post(request, *args, **kwargs)

        use_wp_rte = request.POST.get('use_wp_rte', None)
        wp_prop_flag = request.POST.get('wp_prop_flag', None)
        provers = request.POST.get('provers', None)

        if provers is None:
            request.session['use_wp_rte'] = use_wp_rte
            request.session['wp_prop_flag'] = wp_prop_flag
        else:
            request.session['provers'] = provers

        return redirect('main')
