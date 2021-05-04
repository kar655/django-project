from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User

from frama.models import Directory, File, FileSection


class DirectoryModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user", password="password")
        self.directory = Directory.objects.create(name="My Directory", user=self.user)

    def test_str(self):
        string = str(self.directory)
        self.assertEqual(string, "Directory: My Directory")

    def test_user_ownership(self):
        self.assertEqual(self.directory.user, self.user)

    def test_is_valid(self):
        self.assertTrue(self.directory.is_valid)

    def test_timestamp(self):
        date_format = "%d/%m/%Y"
        self.assertEqual(self.directory.timestamp.strftime(date_format), datetime.now().strftime(date_format))


class FileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user", password="password")
        self.directory = Directory.objects.create(name="My Directory", user=self.user)
        self.file = File.objects.create(name="My File", user=self.user, parent_directory=self.directory)

    def test_str(self):
        string = str(self.file)
        self.assertEqual(string, "File: My File")

    def test_user_ownership(self):
        self.assertEqual(self.file.user, self.user)

    def test_is_valid(self):
        self.assertTrue(self.file.is_valid)

    def test_timestamp(self):
        date_format = "%d/%m/%Y"
        self.assertTrue(self.file.timestamp.strftime(date_format) == datetime.now().strftime(date_format))


class FileSectionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user", password="password")
        self.directory = Directory.objects.create(name="My Directory", user=self.user)
        self.file = File.objects.create(name="My File", user=self.user, parent_directory=self.directory)
        self.file_section = FileSection.objects.create(file_referred=self.file, user=self.user,
                                                       category=FileSection.SectionCategory.LEMMA,
                                                       status=FileSection.SectionStatus.INVALID)

    def test_str(self):
        string = str(self.file_section)
        self.assertEqual(string, "Lemma section of file My File")

    def test_user_ownership(self):
        self.assertEqual(self.file_section.user, self.user)

    def test_is_valid(self):
        self.assertTrue(self.file_section.is_valid)

    def test_timestamp(self):
        date_format = "%d/%m/%Y"
        self.assertTrue(self.file_section.timestamp.strftime(date_format) == datetime.now().strftime(date_format))
