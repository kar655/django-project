from django.db import models


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

    def __str__(self):
        return "File: " + self.name

# class FileSection(BasicInformation):
#     name = models.CharField(max_length=30, blank=True, null=True)
#     description = models.CharField(max_length=100, null=True, blank=True)
