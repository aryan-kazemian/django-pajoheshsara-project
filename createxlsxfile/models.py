from django.db import models
from uuid import uuid4

class TempLink(models.Model):
    link = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    ip = models.GenericIPAddressField()
    file = models.FileField()

    def check_ip(self, ip):
        if self.ip == ip:
            return True
        return False

class XlsxFiles(models.Model):
    name = models.CharField(max_length=100, unique=True)
    file = models.FileField(upload_to='xlsx-files/')

    def __str__(self):
        return self.name

