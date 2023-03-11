from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe, require_http_methods
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from snippets.models import Snippet
from snippets.forms import SnippetForm, CommentForm

# Create your views here.


@require_safe  # GETとHEADメソッドのみ受け付ける
def top(request):
    snippets = Snippet.objects.all()  # snippet一覧取得
    context = {"snippets": snippets}  # てんぷれーとえんじんに与える python object
    return render(request, "snippets/top.html", context)
    # return HttpResponse(b"Hello World")


@login_required
@require_http_methods(["GET", "POST", "HEAD"])  # 指定したメソッドのみ受け付ける
def snippet_new(request):
    if request.method == "POST":
        form = SnippetForm(
            request.POST,
        )
        if form.is_valid():  # DBに登録できるか検証
            snippet = form.save(commit=False)  # セーブしない
            snippet.created_by = request.user
            snippet.save()  # 作成されたモデルをコミット
            return redirect(snippet_detail, snippet_id=snippet.pk)  # 詳細ページに戻す
    else:
        form = SnippetForm()
    return render(request, "snippets/snippet_new.html", {"form": form})
    # return HttpResponse("スニペットの登録")


@login_required
def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    # 自分以外のユーザーの編集を不可にする
    if snippet.created_by_id != request.user.id:
        return HttpResponse("このスニペットの編集は許可されていません")

    if request.method == "POST":
        form = SnippetForm(
            request.POST,
            instance=snippet,  # デフォルト値に snippetを差し込む
        )
        if form.is_valid():
            form.save()  # 編集された部分だけが保存される
            return redirect(snippet_detail, snippet_id=snippet_id)
    else:
        form = SnippetForm(instance=snippet)
    return render(request, "snippets/snippet_edit.html", {"form": form})
    # return HttpResponse("スニペットの編集")


def snippet_detail(request, snippet_id):
    # DBから取り出すときにいつから無ければ404例外を発生する
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    # GET(一覧表示)
    comments = (
        snippet.related_comments.all().order_by("commented_at").reverse()
    )  # 新しい順で
    print("@@@@@@@@", comments)
    form = CommentForm()
    return render(
        request,
        "snippets/snippet_detail.html",
        {"snippet": snippet, "comments": comments, "form": form},
    )
    # return HttpResponse("スニペットの詳細閲覧")


@login_required
def comment_new(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.commented_to = snippet
        comment.commented_by = request.user
        comment.save()
        messages.add_message(request, messages.SUCCESS, "コメントを投稿しました。")
    else:
        messages.add_message(request, messages.ERROR, "コメントの投稿に失敗しました。")
    return redirect("snippet_detail", snippet_id=snippet_id)
