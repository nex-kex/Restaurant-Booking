from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .forms import BookingForm, CategoryForm, TableForm
from .models import Booking, Category, Table


class MainPageTemplateView(TemplateView):
    template_name = "booking/main_page.html"


class AboutPageTemplateView(TemplateView):
    template_name = "booking/about.html"


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("booking:category-list")


class CategoryDetailView(DetailView):
    model = Category


class CategoryListView(ListView):
    model = Category
    context_object_name = "categories"

    # Добавляет в контекст дополнительно количество доступных столиков для каждой категории
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories_with_count = []

        for category in context["categories"]:
            table_count = Table.objects.filter(category=category, is_available=True).count()
            categories_with_count.append({"category": category, "table_count": table_count})
        context["categories_with_count"] = categories_with_count
        return context

    # Возвращает только те категории, в которых есть доступные для брони столы
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(tables__is_available=True).distinct()


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm

    def get_success_url(self):
        return reverse_lazy("booking:category-detail", kwargs={"pk": self.object.pk})


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy("booking:category-list")


class TableCreateView(CreateView):
    model = Table
    form_class = TableForm
    success_url = reverse_lazy("booking:table-list")


class TableDetailView(DetailView):
    model = Table


class TableListView(ListView):
    model = Table

    # Возвращает только те столы, которые доступны для брони
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_available=True)


class TableUpdateView(UpdateView):
    model = Table
    form_class = TableForm

    def get_success_url(self):
        return reverse_lazy("booking:table-detail", kwargs={"pk": self.object.pk})


class TableDeleteView(DeleteView):
    model = Table
    success_url = reverse_lazy("booking:table-list")


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    success_url = reverse_lazy("booking:booking-list")

    # Сразу сохраняет пользователя, без необходимости указывать самостоятельно
    def form_valid(self, form):
        booking_instance = form.save(commit=False)
        user = self.request.user
        booking_instance.user = user
        booking_instance.save()
        return super().form_valid(form)

    # Проверяет, чтобы количество людей не превышало число доступных мест
    def form_invalid(self, form):
        seats = form.cleaned_data.get("people")
        table = form.cleaned_data.get("table")

        if seats and table and seats > table.seats:
            form.add_error(
                "table", f"Стол который вы выбрали рассчитан на {table.seats} мест. Выберете другой столик."
            )

        return self.render_to_response(self.get_context_data(form=form))


class BookingDetailView(DetailView):
    model = Booking


class BookingListView(ListView):
    model = Booking


class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm

    def get_success_url(self):
        return reverse_lazy("booking:booking-detail", kwargs={"pk": self.object.pk})


class BookingDeleteView(DeleteView):
    model = Booking
    success_url = reverse_lazy("booking:booking-list")
