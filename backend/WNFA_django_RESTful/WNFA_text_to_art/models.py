from django.db import models

class Art(models.Model):
    image_binary = models.BinaryField()

    def __str__(self):
        return self.id

class Record(models.Model):
    # id = models.AutoField(primary_key=True)
    request_time = models.TimeField(auto_now_add=True)
    poem_en = models.TextField()
    poem_cn = models.TextField()
    art_id = models.ForeignKey(Art, on_delete=models.CASCADE)

    def __str__(self):
        return self.id