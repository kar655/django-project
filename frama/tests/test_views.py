from http import HTTPStatus
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from parameterized import parameterized
from django.contrib.sessions.middleware import SessionMiddleware

from frama.models import Directory, File
from frama.views import LogoutView, MainView, FileCreateView, FileDeleteView, DirectoryCreateView, DirectoryDeleteView, \
    FileSectionCreateView


class GenerateFileStructureTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user", password="password")
        self.client.force_login(self.user)

        self.root_directory = Directory.objects.create(name="Root directory", user=self.user)
        self.root_directory_file = File.objects.create(name="First file",
                                                       parent_directory=self.root_directory, user=self.user)
        self.child_directory = Directory.objects.create(name="Child directory",
                                                        parent_directory=self.root_directory, user=self.user)
        self.child_directory_file = File.objects.create(name="Second file",
                                                        parent_directory=self.child_directory, user=self.user)


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


class AllViewsGetPostTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user", password="password")
        self.client.force_login(self.user)

    @parameterized.expand([
        ["logout", reverse("logout")],
        ["register", reverse("register")],
        ["main", reverse("main")],
        ["file-add", reverse("file-add")],
        ["file-delete", reverse("file-delete")],
        ["directory-add", reverse("directory-add")],
        ["directory-delete", reverse("directory-delete")],
        ["file-section-add", reverse("file-section-add")],
    ])
    def test_get(self, name, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @parameterized.expand([
        ["logout", reverse("logout")],
        ["register", reverse("register")],
        ["file-add", reverse("file-add")],
        ["file-delete", reverse("file-delete")],
        ["directory-add", reverse("directory-add")],
        ["directory-delete", reverse("directory-delete")],
        ["file-section-add", reverse("file-section-add")],
    ])
    def test_post(self, name, url):
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class DirectoryDeleteViewTest(GenerateFileStructureTests):

    def setUp(self):
        super(DirectoryDeleteViewTest, self).setUp()
        self.url = reverse("directory-delete")

        self.form_data = {
            "directory": None,
        }

    def make_form(self):
        self.form = DirectoryDeleteView.form_class(self.form_data, user_id=self.user.id)

    def generic_delete_directory(self, directory):
        self.form_data["directory"] = directory
        self.make_form()
        self.assertTrue(self.form.is_valid())

        DirectoryDeleteView().form_valid(self.form)

    def test_delete_child_directory(self):
        self.generic_delete_directory(self.child_directory)

        self.assertFalse(Directory.objects.get(pk=self.child_directory.pk).is_valid)
        self.assertFalse(File.objects.get(pk=self.child_directory_file.pk).is_valid)

    def test_delete_root_directory(self):
        self.generic_delete_directory(self.root_directory)

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


class FileDeleteViewTest(GenerateFileStructureTests):

    def setUp(self):
        super(FileDeleteViewTest, self).setUp()
        self.url = reverse("file-delete")

        self.form_data = {
            "file": None,
        }

    def make_form(self):
        self.form = FileDeleteView.form_class(self.form_data, user_id=self.user.id)

    def generic_delete_files(self, file):
        self.form_data["file"] = file
        self.make_form()
        self.assertTrue(self.form.is_valid())

        FileDeleteView().form_valid(self.form)

        self.assertFalse(File.objects.get(pk=file.pk).is_valid)

    def test_delete_child_file(self):
        self.generic_delete_files(self.child_directory_file)

    def test_delete_root_file(self):
        self.generic_delete_files(self.root_directory_file)


class MainViewTest(GenerateFileStructureTests):

    def setUp(self):
        super(MainViewTest, self).setUp()
        # self.url = reverse("main")

    def test_no_file_chosen(self):
        url = reverse("main")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Please choose a file", html=True)

        # Test get_context_data
        self.assertIsNotNone(response.context['recursive_structure'])
        self.assertIsNone(response.context['chosen_file'])
        self.assertIsNone(response.context['file_elements_sections'])
        self.assertIsNone(response.context['line_tooltips'])
        self.assertIsNone(response.context['file_content'])
        self.assertIsNotNone(response.context['chosen_tab'])
        self.assertIsNotNone(response.context['is_result'])

        # Test used templates
        self.assertTemplateUsed(response, "frama/index.html")
        self.assertTemplateUsed(response, "frama/directory_tree_recursive.html")
        self.assertTemplateUsed(response, "frama/file_content.html")
        self.assertTemplateUsed(response, "frama/program_elements.html")
        self.assertTemplateUsed(response, "frama/tab_data.html")
