from django.db import models


class Image(models.Model):
    # https://qiita.com/honda28/items/4a37e951059d74fcf9f1
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.title
