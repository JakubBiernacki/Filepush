from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.crypto import get_random_string
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dir_{self.code}_{self.user}"

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

    def __str__(self):
        return self.file.name

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    @property
    def filesize(self):
        size = self.file.size
        return round(size / 1048576, 2)


@receiver(post_delete, sender=File)
def delete_file(sender, instance, **kwargs):
    try:
        os.remove(instance.file.path)
    except FileNotFoundError:
        pass


class DownloadData(models.Model):
    user = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    file = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)


# User additional method
@property
def folders_count(self):
    return self.sharedir_set.count()


@property
def all_file_size(self):
    dirs = self.sharedir_set.prefetch_related('file_set')
    size = 0
    for dir in dirs:
        size += dir.size
    return size


User.add_to_class('folders_count', folders_count)
User.add_to_class('all_file_size', all_file_size)


@receiver(post_save, sender=User)
def add_new_user_to_group(sender, instance, created, **kwargs):
    if created:
        # instance.is_active = False
        group = Group.objects.get(id=1)
        instance.groups.add(group)
        instance.save()
