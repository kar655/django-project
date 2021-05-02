from django import forms
from enum import Enum, unique
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as DjangoUser

from .models import User, File, Directory, FileSection


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = DjangoUser
        fields = ["username", "email", "password1", "password2"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        widgets = {
            "password": forms.PasswordInput()
        }


class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        fields = "__all__"
        exclude = ["timestamp", "is_valid", "user"]

    def __init__(self, *args, **kwargs):
        super(DirectoryForm, self).__init__(*args, **kwargs)
        self.fields["parent_directory"].queryset = Directory.objects.filter(is_valid=True)


class DirectoryDeleteForm(forms.Form):
    directory = forms.ModelChoiceField(queryset=Directory.objects.filter(is_valid=True))


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = "__all__"
        exclude = ["timestamp", "is_valid", "user"]

    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        self.fields["parent_directory"].queryset = Directory.objects.filter(is_valid=True)


class FileDeleteForm(forms.Form):
    file = forms.ModelChoiceField(queryset=File.objects.filter(is_valid=True))


class FileSectionForm(forms.ModelForm):
    class Meta:
        model = FileSection
        fields = "__all__"
        exclude = ["timestamp", "is_valid", "user"]

    def __init__(self, *args, **kwargs):
        super(FileSectionForm, self).__init__(*args, **kwargs)
        self.fields["file_referred"].queryset = File.objects.filter(is_valid=True)


class TabProversForm(forms.Form):
    provers = forms.ChoiceField(choices=(
        ("alt-ergo", "Alt-Ergo"),
        ("z3", "Z3"),
        ("cvc4", "CVC4"),
    ))

    def add_to_session(self, session):
        session['provers'] = self.cleaned_data['provers']


class TabVCsForm(forms.Form):
    use_wp_rte = forms.BooleanField(required=False)
    wp_prop_flag = forms.CharField(required=False, max_length=30)

    def add_to_session(self, session):
        session['use_wp_rte'] = self.cleaned_data['use_wp_rte']
        session['wp_prop_flag'] = self.cleaned_data['wp_prop_flag']


@unique
class ChosenTab(str, Enum):
    PROVERS = "provers"
    VCS = "vcs"
    RESULT = "result"

    @staticmethod
    def give_form(value):
        if value == ChosenTab.PROVERS:
            return TabProversForm
        elif value == ChosenTab.VCS:
            return TabVCsForm
        else:
            def get_tab_results(provers, use_wp_rte, wp_prop_flag, file_path):
                if wp_prop_flag is None or len(wp_prop_flag) == 0:
                    wp_prop_flag = None
                else:
                    wp_prop_flag = "\"" + wp_prop_flag + "\""

                return f"frama-c -wp{f' -wp-prover {provers}' if provers is not None else ''}{f' -wp-prop={wp_prop_flag}' if wp_prop_flag else ''}{' -wp-rte' if use_wp_rte else ''} -wp-log=\"r:result.txt\" {file_path}"

            return get_tab_results

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
