from django.contrib import admin
from api.users.models import Users, Session


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username')


class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'active')


admin.site.register(Users, UsersAdmin)
admin.site.register(Session, SessionAdmin)
