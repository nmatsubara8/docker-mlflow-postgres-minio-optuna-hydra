# from django.test import TestCase
# Create your tests here.
import pytest
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase, Client, RequestFactory
from django.urls import resolve
from snippets.views import top, snippet_detail, snippet_edit, snippet_new
from snippets.models import Snippet

UserModel = get_user_model()


class CreateSnippetTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="test_password_0001",
        )
        self.client.force_login(self.user)  # ユーザーログイン

    def test_render_creation_form(self):
        response = self.client.get("/snippets/new/")
        self.assertContains(response, "スニペットの登録", status_code=200)

    def test_create_snippet(self):
        data = {"title": "タイトル", "code": "コード", "description": "解説"}
        self.client.post("/snippets/new/", data)
        snippet = Snippet.objects.get(title="タイトル")
        self.assertEqual("コード", snippet.code)
        self.assertEqual("解説", snippet.description)

    def test_should_resolve_snippet_new(self):
        found = resolve("/snippets/new/")
        self.assertEqual(snippet_new, found.func)


class SnippetDetailTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="test_password_0001",
        )
        self.snippet = Snippet.objects.create(
            title="title",
            code="print('hello')",
            description="description",
            created_by=self.user,
        )

    def test_should_use_expected_template(self):
        # 末尾の / を忘れない！！！！！！！！
        response = self.client.get(f"/snippets/{self.snippet.id}/")
        print(response)
        self.assertTemplateUsed(
            response, "snippets/snippet_detail.html"
        )  # 意図したテンプレートが使われているか

    def test_top_page_returns_200_and_expected_heading(self):
        response = self.client.get(f"/snippets/{self.snippet.id}/")
        self.assertContains(response, self.snippet.title, status_code=200)

    def test_should_resolve_snippet_detail(self):
        found = resolve("/snippets/1/")
        self.assertEqual(snippet_detail, found.func)


class EditSnippetTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="test_password_0001",
        )
        self.snippet = Snippet.objects.create(
            title="title",
            code="print('hello')",
            description="description",
            created_by=self.user,
        )
        self.client.force_login(self.user)  # ユーザーログイン

    def test_render_edit_form(self):
        response = self.client.get(f"/snippets/{self.snippet.id}/edit/")
        self.assertContains(response, "スニペットの編集", status_code=200)

    def test_edit_snippet(self):
        data = {"title": "タイトル2", "code": "コード2", "description": "解説2"}
        self.client.post(f"/snippets/{self.snippet.id}/edit/", data)
        snippet = Snippet.objects.get(title="タイトル2")
        self.assertEqual("コード2", snippet.code)
        self.assertEqual("解説2", snippet.description)

    def test_should_resolve_snippet_edit(self):
        found = resolve("/snippets/1/edit/")
        self.assertEqual(snippet_edit, found.func)


# class TopPageViewTest(TestCase):
#     def test_top_returns_200(self):
#         response = self.client.get("/")
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Django")

#     def test_top_returns_expected_content(self):
#         response = self.client.get("/")
#         self.assertEqual(response.content.decode("utf-8"), "Hello World")


class TopPageTest(TestCase):
    def test_top_page_returns_200_and_expected_title(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django", status_code=200)

    def test_top_page_uses_expected_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "snippets/top.html")


class TopPageRenderSnippetsTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="test_password_0001",
        )
        self.snippet = Snippet.objects.create(
            title="title",
            code="print('hello')",
            description="description",
            created_by=self.user,
        )

    def test_should_return_snippet_title(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.snippet.title)

    def test_should_return_username(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.user.username)
