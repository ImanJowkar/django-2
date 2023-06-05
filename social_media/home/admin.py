from django.contrib import admin
from . import models
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['created', 'user','slug'] 
    search_fields = ['slug',]
    list_filter = ['updated']

    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)




admin.site.register(models.Post, PostAdmin)