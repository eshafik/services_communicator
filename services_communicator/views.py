# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
	ServiceList,
)


class ServiceListCreateView(CreateView):

    model = ServiceList


class ServiceListDeleteView(DeleteView):

    model = ServiceList


class ServiceListDetailView(DetailView):

    model = ServiceList


class ServiceListUpdateView(UpdateView):

    model = ServiceList


class ServiceListListView(ListView):

    model = ServiceList

