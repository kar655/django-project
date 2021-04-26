from django.db import models
from django.utils.translation import gettext_lazy


class User(models.Model):
    login = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=50, help_text="Stored each password as an encrypted text")

    def __str__(self):
        return self.login


class BasicInformation(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)


class Directory(BasicInformation):
    name = models.CharField(max_length=30, primary_key=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_directory = models.ForeignKey('Directory', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "Directory: " + self.name


class File(BasicInformation):
    name = models.CharField(max_length=30, primary_key=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_directory = models.ForeignKey(Directory, on_delete=models.CASCADE, null=True, blank=True)
    file_field = models.FileField(upload_to="uploads/")

    def __str__(self):
        return "File: " + self.name


# class SectionData(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     status_data = models.CharField(max_length=100)


class FileSection(BasicInformation):
    file_referred = models.ForeignKey(File, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    class SectionCategory(models.TextChoices):
        PROCEDURE = "Procedure", gettext_lazy("Procedure")
        PROPERTY = "Property", gettext_lazy("Property")
        LEMMA = "Lemma", gettext_lazy("Lemma")
        ASSERTION = "Assertion", gettext_lazy("Assertion")
        INVARIANT = "Invariant", gettext_lazy("Invariant")
        PRECONDITION = "Precondition", gettext_lazy("Precondition")
        POSTCONDITION = "Postcondition", gettext_lazy("Postcondition")

    category = models.CharField(
        max_length=13,
        choices=SectionCategory.choices,
    )

    class SectionStatus(models.TextChoices):
        PROVED = "Proved", gettext_lazy("Proved")
        INVALID = "Invalid", gettext_lazy("Invalid")
        COUNTEREXAMPLE = "Counterexample", gettext_lazy("Counterexample")
        UNCHECKED = "Unchecked", gettext_lazy("Unchecked")

    status = models.CharField(
        max_length=14,
        choices=SectionStatus.choices,
    )

    status_data = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.category + " section of file " + self.file_referred.name
