# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import (
   ServiceList,
)


@admin.register(ServiceList)
class ServiceListAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'service_guid', 'service_id']
    prepopulated_fields = {"service_slug": ("service_name",)}



