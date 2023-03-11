# from django.contrib.auth.forms import UserCreationForm
from .admin import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import CreateView
from .views import EmailVerificationSentView


# クラスベースビュー
# as_view で関数のように呼び出せる
# 実装済みの login, logout view クラスを使用する
# signup は、汎用ビューを作成できる CreateViewを使用
urlpatterns = [
    # path(
    #     "signup/",
    #     CreateView.as_view(
    #         template_name="account/signup.html",
    #         form_class=UserCreationForm,  # 使用する formクラス。ユーザー作成用フォームの UserCreationFormを使用
    #         success_url="/",
    #     ),
    #     name="signup",
    # ),
    # path(
    #     "login/",
    #     LoginView.as_view(
    #         redirect_authenticated_user=True,  # ログイン済みならログイン画面を表示せず、トップページなどにリダイレクト
    #         template_name="account/login.html",
    #     ),
    #     name="login",
    # ),
    # path("logout/", LogoutView.as_view(), name="logout"),
    # path(
    #     "confirm-email/",
    #     EmailVerificationSentView.as_view(),
    #     name="account_email_verification_sent",
    # ),
]
