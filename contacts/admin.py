# coding=utf-8
__author__ = 'renkse'

from django.contrib import admin
from models import Contact, ContactPhone, FeedbackMessage, WorkTime

admin.autodiscover()


class PhoneInline(admin.TabularInline):
    model = ContactPhone
    extra = 0


class WorkTimeInline(admin.TabularInline):
    model = WorkTime
    extra = 0


class ContactAdmin(admin.ModelAdmin):
    inlines = [PhoneInline, WorkTimeInline]

    # def has_add_permission(self, request, obj=None):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'message', 'branch', 'received_at')
    readonly_fields = ('name', 'phone', 'email', 'message', 'branch', 'received_at')

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Contact, ContactAdmin)
admin.site.register(FeedbackMessage, FeedbackAdmin)