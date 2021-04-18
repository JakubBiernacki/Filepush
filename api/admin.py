from django.contrib import admin
from .models import Sharedir, File

# Register your models here.



@admin.register(Sharedir)
class SharedirAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'code', 'created_at', 'size', 'count']

    def size(self, obj):
        return f"{obj.size} MB"

    def count(self, obj):
        return obj.file_set.count()
    # list_filter = ['obrazek']
    # search_fields = ['tresc']

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename', 'dir', 'filesize']

    def filesize(self, obj):
        return f"{obj.filesize} MB"