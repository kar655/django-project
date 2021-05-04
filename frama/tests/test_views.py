from http import HTTPStatus
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from parameterized import parameterized
from django.contrib.sessions.middleware import SessionMiddleware

from frama.models import Directory, File
from frama.views import LogoutView, MainView, FileCreateView, FileDeleteView, DirectoryCreateView, DirectoryDeleteView, \
    FileSectionCreateView


# class TestViewWithUser(TestCase):
#
#     def setUp(self):
#         self.user = User.objects.create(username="user", password="password")
#         self.factory = RequestFactory()
#         self.middleware = SessionMiddleware()
#
#     def generate_request(self, url, get=True, data=None):
#         request = self.factory.get(url, data=data) if get else self.factory.post(url, data=data)
#         self.middleware.process_request(request)
#         request.session.save()
#         request.user = self.user
#
#         return request


class RequiresLoginViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user", password="password")
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def generate_request(self, url, post=False):
        request = self.factory.post(url) if post else self.factory.get(url)
        self.middleware.process_request(request)
        request.session.save()
        return request

    @parameterized.expand([
        ["logout", reverse("logout")],
        ["main", reverse("main")],
        ["file-add", reverse("file-add")],
        ["file-delete", reverse("file-delete")],
        ["directory-add", reverse("directory-add")],
        ["directory-delete", reverse("directory-delete")],
        ["file-section-add", reverse("file-section-add")],
    ])
    def test_logout_redirect(self, name, url):
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + "?next=" + url)

    @parameterized.expand([
        ["logout", reverse("logout"), LogoutView],
        ["main", reverse("main"), MainView],
        ["file-add", reverse("file-add"), FileCreateView],
        ["file-delete", reverse("file-delete"), FileDeleteView],
        ["directory-add", reverse("directory-add"), DirectoryCreateView],
        ["directory-delete", reverse("directory-delete"), DirectoryDeleteView],
        ["file-section-add", reverse("file-section-add"), FileSectionCreateView],
    ])
    def test_logged_user(self, name, url, class_view):
        request = self.generate_request(url)
        request.user = self.user
        response = class_view.as_view()(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class MainViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user", password="password")


class DirectoryDeleteViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user", password="password")
        self.url = reverse("directory-delete")
        self.root_directory = Directory.objects.create(name="Root directory", user=self.user)
        self.root_directory_file = File.objects.create(name="First file",
                                                       parent_directory=self.root_directory, user=self.user)
        self.child_directory = Directory.objects.create(name="Child directory",
                                                        parent_directory=self.root_directory, user=self.user)
        self.child_directory_file = File.objects.create(name="Second file",
                                                        parent_directory=self.child_directory, user=self.user)
        self.form_data = {
            "directory": None,
        }

        self.client.force_login(self.user)

    def make_form(self):
        self.form = DirectoryDeleteView.form_class(self.form_data, user_id=self.user.id)

    def test_delete_child_directory(self):
        self.form_data["directory"] = self.child_directory
        self.make_form()
        self.assertTrue(self.form.is_valid())

        DirectoryDeleteView().form_valid(self.form)

        self.assertFalse(Directory.objects.get(pk=self.child_directory.pk).is_valid)
        self.assertFalse(File.objects.get(pk=self.child_directory_file.pk).is_valid)

    def test_delete_root_directory(self):
        self.form_data["directory"] = self.root_directory
        self.make_form()
        self.assertTrue(self.form.is_valid())

        DirectoryDeleteView().form_valid(self.form)

        self.assertFalse(Directory.objects.get(pk=self.root_directory.pk).is_valid)
        self.assertFalse(File.objects.get(pk=self.root_directory_file.pk).is_valid)
        self.assertFalse(Directory.objects.get(pk=self.child_directory.pk).is_valid)
        self.assertFalse(File.objects.get(pk=self.child_directory_file.pk).is_valid)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_test(self):
        # request = self.generate_request(self.url)
        # response = DirectoryDeleteView.as_view()(request)
        # print(response)
        #
        # self.form_data["directory"] = self.child_directory
        # self.form_data["directory"] = "nonsense"
        # request = self.generate_request(self.url, get=False, data=self.form_data)
        # response = DirectoryDeleteView.as_view()(request)
        # print(response)

        # print(self.client.login(username=self.user.username, password="password"))
        #
        # self.client.force_login(self.user)
        # response = self.client.post(self.url, data=self.form_data)
        # print(response)
        # print(response.context['form'].is_valid())
        # print(response.templates[0].name)
        # print(self.child_directory.is_valid)

        # self.client.force_login(self.user)
        pass
