from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .forms import BookingForm, CategoryForm, TableForm
from .models import Booking, Category, Table


class MainPageTemplateView(TemplateView):
    template_name = "booking/main_page.html"


class AboutPageTemplateView(TemplateView):
    template_name = "booking/about.html"


class BookingPageTemplateView(TemplateView):
    template_name = "booking/book.html"


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = "booking:main"


class CategoryDetailView(DetailView):
    model = Category


class CategoryListView(ListView):
    model = Category


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = "booking:main"


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "booking:main"


class TableCreateView(CreateView):
    model = Table
    form_class = TableForm
    success_url = "booking:main"


class TableDetailView(DetailView):
    model = Table


class TableListView(ListView):
    model = Table


class TableUpdateView(UpdateView):
    model = Table
    form_class = TableForm
    success_url = "booking:main"


class TableDeleteView(DeleteView):
    model = Table
    success_url = "booking:main"


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    success_url = "booking:main"


class BookingDetailView(DetailView):
    model = Booking


class BookingListView(ListView):
    model = Booking


class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    success_url = "booking:main"


class BookingDeleteView(DeleteView):
    model = Booking
    success_url = "booking:main"
