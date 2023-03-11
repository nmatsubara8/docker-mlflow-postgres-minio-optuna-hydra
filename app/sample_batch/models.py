from django.db import models


class MSYSModel(models.Model):
    run_id = models.CharField("run_id", max_length=128)
    experiment_id = models.CharField("experiment_id", max_length=128)
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return f"run_id: {self.run_id} experiment_id:{self.experiment_id}"
