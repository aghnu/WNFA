from django.db import models

class Art(models.Model):
    data = models.BinaryField()

class Record(models.Model):
    request_time = models.DateTimeField(auto_now_add=True)
    poem_en = models.TextField()
    poem_cn = models.TextField()
    art_id = models.IntegerField()

    class Meta:
        ordering = ['-request_time']