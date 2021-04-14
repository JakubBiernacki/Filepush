import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string

from django.db.models.signals import post_delete
import os


def generate_code():
    while True:
        code = get_random_string(6)

        if not Sharedir.objects.filter(code=code).exists():
            break
    return code


class Sharedir(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True, default=generate_code)
    creared_at = models.DateTimeField(auto_now_add=True)

    @property
    def delete_at(self):
        return self.creared_at + datetime.timedelta(days=2)

    @property
    def file_count(self):
        return self.file_set.count()

    @property
    def size(self):
        files = self.file_set.all()

        size = 0
        for f in files:
            size += f.file.size

        return round(size / 1048576, 2)


class File(models.Model):
    file = models.FileField(upload_to='pliki/%Y-%m-%d', blank=False)
    dir = models.ForeignKey(Sharedir, on_delete=models.CASCADE)


def delete_file(sender, instance, **kwargs):
    try:
        os.remove(instance.file.path)
    except FileNotFoundError:
        pass


post_delete.connect(delete_file, sender=File)
