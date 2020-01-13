# -*- coding: utf-8 -*-
import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.template.defaultfilters import slugify

from model_utils.models import TimeStampedModel


class ServiceList(TimeStampedModel):
    service_name = models.CharField(max_length=45)
    service_guid = models.CharField(max_length=45, default=uuid.uuid4)
    service_slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
    service_id = models.PositiveSmallIntegerField()
    service_url = models.URLField(blank=True, null=True)
    api_version = models.CharField(max_length=10, blank=True, null=True)
    service_token_url = models.CharField(max_length=50, default="/users/token/")
    service_details = JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.service_slug = slugify(self.service_name)
        super(ServiceList, self).save(*args, **kwargs)

    @property
    def get_full_url(self):
        """
            -getting full base url with api version
        """
        return self.service_url + self.api_version

    def __str__(self):
        return self.service_name

    class Meta:
        ordering = ['-created_at']
