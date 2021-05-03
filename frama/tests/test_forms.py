from http import HTTPStatus
from django.test import TestCase
from django.contrib.auth.models import User

from frama.models import Directory
from frama.forms import RegisterForm, DirectoryForm


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

    def test_email_missing(self):
        self.form_data.pop("email")
        form = RegisterForm(self.form_data)
        self.assertFalse(form.is_valid())

    def test_correct_form(self):
        form = RegisterForm(self.form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, self.form_data["username"])
        self.assertEqual(user.email, self.form_data["email"])


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
