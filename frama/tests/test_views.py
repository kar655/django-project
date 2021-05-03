from http import HTTPStatus
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from parameterized import parameterized
from django.contrib.sessions.middleware import SessionMiddleware

from frama.models import Directory, File
from frama.views import LogoutView, MainView, FileCreateView, FileDeleteView, DirectoryCreateView, DirectoryDeleteView, \
    FileSectionCreateView


class RequiresLoginViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user", password="password")
        self.factory = RequestFactory()
        self.middleware = SessionMiddleware()

    def generate_request(self, url):
        request = self.factory.get(url)
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
        self.factory = RequestFactory()
        self.user = User.objects.create(username="user", password="password")
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

    def make_form(self):
        self.form = DirectoryDeleteView.form_class(self.form_data)

    def test_delete_child_directory(self):
        #         # Create an instance of a GET request.
        #         request = self.factory.get('/customer/details')
        #
        #         # Recall that middleware are not supported. You can simulate a
        #         # logged-in user by setting request.user manually.
        #         request.user = self.user
        #
        #         # Or you can simulate an anonymous user by setting request.user to
        #         # an AnonymousUser instance.
        #         request.user = AnonymousUser()
        #
        #         # Test my_view() as if it were deployed at /customer/details
        #         response = my_view(request)
        #         # Use this syntax for class-based views.
        #         response = MyView.as_view()(request)
        #         self.assertEqual(response.status_code, 200)
        # self.form_data["directory"] = self.child_directory
        #
        # request = self.factory.get(reverse("directory-delete"))
        # # request.user = self.user
        #
        # response = DirectoryDeleteView.as_view()(request)
        # print(response)
        # self.assertEqual(response.status_code, HTTPStatus.OK)
        pass
