from django.contrib import admin

# Register your models here.
from .models import adminPost, dkTopic, allReply, topicTheme, Notes

admin.site.register(adminPost)
admin.site.register(dkTopic)
admin.site.register(allReply)
admin.site.register(topicTheme)
admin.site.register(Notes)