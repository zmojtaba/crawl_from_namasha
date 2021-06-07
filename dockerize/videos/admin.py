from .models import *
from django.contrib import admin

class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'category', 'channel']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class ChannelAdmin(admin.ModelAdmin):
    list_display = ['title', 'link']
    search_fields = ['link']


class Channel_VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'link']


admin.site.register(Video, VideoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Channel_Video, Channel_VideoAdmin)

