from django.views.decorators.http import require_safe, require_http_methods
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse

from PIL import Image
import json

# Create your views here.
@require_safe  # GETとHEADメソッドのみ受け付ける
def search(request):
    # snippets = Snippet.objects.all()  # snippet一覧取得
    # context = {"snippets": snippets}  # てんぷれーとえんじんに与える python object
    # img = Image.open("")
    path = "/app/viewer/static/img/20190510_0100_01_00596.png"
    json_path = "/app/viewer/static/img/20190510_0100_01_00596.json"
    img = Image.open(path)
    with open(json_path) as json_data:
        data = json.load(json_data)
    print(data)
    print(img.width)
    context = {"img_path": path, "width": img.width, "height": img.height, "json_data": data}

    return render(request, "viewer/viewer.html", context)
    # return HttpResponse(b"Hello World")


@require_safe  # GETとHEADメソッドのみ受け付ける
def canvas_image(request, image_path):
    """canvasへ渡す画像を取得する
    TODO: image_path を image_id にしたほうが良い?
    Args:
        request (_type_): _description_
        image_path (_type_): _description_
    """
    response = FileResponse(open(image_path, "rb"))
    # response['contents_type'] = 'application'
    return response
