from django import forms
from enum import Enum, unique

from .models import User, File, Directory, FileSection


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
        ("Alt-Ergo", "Alt-Ergo"),
        ("Z3", "Z3"),
        ("CVC4", "CVC4"),
    ))

    def clean_prover(self):
        data = self.cleaned_data['provers']
        print(f"SAVING {data}")

        return data


class TabVCsForm(forms.Form):
    vcs = forms.ChoiceField(choices=(
        ("Opcja 1", "Opcja 1"),
        ("Opcja 2", "Opcja 2"),
    ))

    def clean_vc(self):
        data = self.cleaned_data['vcs']
        print(f"SAVING {data}")

        return data


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
            def get_tab_results(provers, vcs, file_path):
                return f"frama-c -wp -wp-prover {provers} -wp-prop={vcs} {file_path}"

            return get_tab_results

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
