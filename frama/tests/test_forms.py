from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from frama.models import Directory, File, FileSection
from frama.forms import RegisterForm, DirectoryForm, DirectoryDeleteForm, FileForm, \
    FileDeleteForm, FileSectionForm, TabProversForm, TabVCsForm


# TODO add tests with is_valid = False

class RegisterFormTest(TestCase):

    def setUp(self):
        self.form_data = {
            "username": "User",
            "email": "my-email@gmail.com",
            "password1": "amazing_password",
            "password2": "amazing_password",
        }

    def test_empty_form(self):
        form = RegisterForm()
        self.assertFalse(form.is_valid())

    def test_correct_form(self):
        form = RegisterForm(self.form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, self.form_data["username"])
        self.assertEqual(user.email, self.form_data["email"])

    def test_email_missing(self):
        self.form_data.pop("email")
        form = RegisterForm(self.form_data)
        self.assertFalse(form.is_valid())


class DirectoryFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user", password="password")
        self.parent_directory = Directory.objects.create(name="Parent Directory", user=self.user)
        self.form_data = {
            "name": "New Directory",
            "description": "My Long Description",
            "parent_directory": self.parent_directory,
        }

    def test_empty_form(self):
        form = DirectoryForm(user_id=self.user.id)
        self.assertFalse(form.is_valid())

    def test_correct_form(self):
        form = DirectoryForm(self.form_data, user_id=self.user.id)
        self.assertTrue(form.is_valid())

    def test_only_necessary_values(self):
        self.form_data.pop("description")
        self.form_data.pop("parent_directory")
        form = DirectoryForm(self.form_data, user_id=self.user.id)
        self.assertTrue(form.is_valid())

    def test_user_id_missing(self):
        self.assertRaises(KeyError, DirectoryForm, self.form_data)

    def test_second_user(self):
        second_user = User.objects.create(username="second", password="password")
        second_user_directory = Directory.objects.create(name="Not My Directory", user=second_user)

        self.form_data["parent_directory"] = second_user_directory
        form = DirectoryForm(self.form_data, user_id=self.user.id)
        self.assertFalse(form.is_valid())


class DirectoryDeleteFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user", password="password")
        self.directory = Directory.objects.create(name="Directory", user=self.user)
        self.form_data = {
            "directory": self.directory,
        }

    def test_empty_form(self):
        form = DirectoryDeleteForm(user_id=self.user.id)
        self.assertFalse(form.is_valid())

    def test_correct_form(self):
        form = DirectoryDeleteForm(self.form_data, user_id=self.user.id)
        self.assertTrue(form.is_valid())

    def test_user_id_missing(self):
        self.assertRaises(KeyError, DirectoryDeleteForm, self.form_data)

    def test_second_user(self):
        second_user = User.objects.create(username="second", password="password")
        second_user_directory = Directory.objects.create(name="Not My Directory", user=second_user)

        self.form_data["directory"] = second_user_directory
        form = DirectoryDeleteForm(self.form_data, user_id=self.user.id)
        self.assertFalse(form.is_valid())


class FileFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user", password="password")
        self.parent_directory = Directory.objects.create(name="Parent Directory", user=self.user)
        self.form_data = {
            "name": "New File",
            "description": "My Long Description",
            "parent_directory": self.parent_directory,
        }
        self.form_files = {
            "file_field": SimpleUploadedFile("uploaded.txt", b"Hello World!\n"),
        }

    def test_empty_form(self):
        form = FileForm(user_id=self.user.id)
        self.assertFalse(form.is_valid())

    def test_correct_form(self):
        form = FileForm(self.form_data, files=self.form_files, user_id=self.user.id)
        self.assertTrue(form.is_valid())

    def test_user_id_missing(self):
        self.assertRaises(KeyError, FileForm, self.form_data)

    def test_only_necessary_values(self):
        self.form_data.pop("description")
        form = FileForm(self.form_data, files=self.form_files, user_id=self.user.id)
        self.assertTrue(form.is_valid())

    def test_second_user(self):
        second_user = User.objects.create(username="second", password="password")
        second_user_directory = Directory.objects.create(name="Not My Directory", user=second_user)

        self.form_data["parent_directory"] = second_user_directory
        form = FileForm(self.form_data, files=self.form_files, user_id=self.user.id)
        self.assertFalse(form.is_valid())

    def test_missing_files(self):
        form = FileForm(self.form_data, user_id=self.user.id)
        self.assertFalse(form.is_valid())


class FileDeleteFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user", password="password")
        self.parent_directory = Directory.objects.create(name="Directory", user=self.user)
        self.file = File.objects.create(name="File", user=self.user, parent_directory=self.parent_directory)
        self.form_data = {
            "file": self.file,
        }

    def test_empty_form(self):
        form = FileDeleteForm(user_id=self.user.id)
        self.assertFalse(form.is_valid())

    def test_correct_form(self):
        form = FileDeleteForm(self.form_data, user_id=self.user.id)
        self.assertTrue(form.is_valid())

    def test_user_id_missing(self):
        self.assertRaises(KeyError, FileDeleteForm, self.form_data)

    def test_second_user(self):
        second_user = User.objects.create(username="second", password="password")
        second_user_directory = Directory.objects.create(name="Not My Directory", user=second_user)
        second_user_file = File.objects.create(name="Not My File",
                                               user=second_user, parent_directory=second_user_directory)

        self.form_data["file"] = second_user_file
        form = FileDeleteForm(self.form_data, user_id=self.user.id)
        self.assertFalse(form.is_valid())


class FileSectionFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user", password="password")
        self.parent_directory = Directory.objects.create(name="Parent Directory", user=self.user)
        self.file = File.objects.create(name="File", user=self.user, parent_directory=self.parent_directory)
        self.form_data = {
            "file_referred": self.file,
            "name": "New FileSection",
            "description": "My Long Description",
            "category": FileSection.SectionCategory.PRECONDITION,
            "status": FileSection.SectionStatus.PROVED,
            "status_data": "My status data",
        }

    def test_empty_form(self):
        form = FileSectionForm(user_id=self.user.id)
        self.assertFalse(form.is_valid())

    def test_correct_form(self):
        form = FileSectionForm(self.form_data, user_id=self.user.id)
        self.assertTrue(form.is_valid())

    def test_user_id_missing(self):
        self.assertRaises(KeyError, FileSectionForm, self.form_data)

    def test_only_necessary_values(self):
        self.form_data.pop("name")
        self.form_data.pop("description")
        self.form_data.pop("status_data")
        form = FileSectionForm(self.form_data, user_id=self.user.id)
        self.assertTrue(form.is_valid())
        # Todo add parametrized with missing one of necessary value

    def test_second_user(self):
        second_user = User.objects.create(username="second", password="password")
        second_user_directory = Directory.objects.create(name="Not My Directory", user=second_user)
        second_user_file = File.objects.create(name="Not My File",
                                               user=second_user, parent_directory=second_user_directory)

        self.form_data["file_referred"] = second_user_file
        form = FileSectionForm(self.form_data, user_id=self.user.id)
        self.assertFalse(form.is_valid())


class TabProversFormTest(TestCase):

    def setUp(self):
        self.form_data = {
            "provers": "alt-ergo",
        }

    def test_empty_form(self):
        form = TabProversForm()
        self.assertFalse(form.is_valid())

    def test_correct_form(self):
        form = TabProversForm(self.form_data)
        self.assertTrue(form.is_valid())

    def test_add_to_session(self):
        form = TabProversForm(self.form_data)
        self.assertTrue(form.is_valid())
        session = self.client.session
        form.add_to_session(session)
        session.save()

        self.assertIn("provers", self.client.session)
        self.assertEqual(session["provers"], self.form_data["provers"])


class TabVCsFormTest(TestCase):

    def setUp(self):
        self.form_data = {
            "use_wp_rte": True,
            "wp_prop_flag": "INVARIANT",
        }

    def test_empty_form(self):
        form = TabVCsForm({})
        self.assertTrue(form.is_valid())

    def test_correct_form(self):
        form = TabVCsForm(self.form_data)
        self.assertTrue(form.is_valid())

    def test_add_to_session(self):
        form = TabVCsForm(self.form_data)
        self.assertTrue(form.is_valid())
        session = self.client.session
        form.add_to_session(session)
        session.save()

        self.assertIn("use_wp_rte", self.client.session)
        self.assertEqual(session["use_wp_rte"], self.form_data["use_wp_rte"])
        self.assertIn("wp_prop_flag", self.client.session)
        self.assertEqual(session["wp_prop_flag"], self.form_data["wp_prop_flag"])
