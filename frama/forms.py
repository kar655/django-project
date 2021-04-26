from django import forms

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
