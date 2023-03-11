from django import forms
from snippets.models import Snippet, Comment


class SnippetForm(forms.ModelForm):
    """フォーム
    validation も追加できる。
    """

    class Meta:
        # フォームで使う属性を定義
        model = Snippet
        fields = ("title", "code", "description")


class CommentForm(forms.ModelForm):
    """フォーム
    validation も追加できる。
    """

    class Meta:
        # フォームで使う属性を定義
        model = Comment
        fields = ("text",)
        labels = {
            "text": "",
        }
