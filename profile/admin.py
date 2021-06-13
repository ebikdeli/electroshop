from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import Profile


class ProfileInlineAdmin(admin.StackedInline):
    model = Profile


class UserAdmin(AuthUserAdmin):
    inlines = [ProfileInlineAdmin]


admin.site.unregister(User)

admin.site.register(User, UserAdmin)
