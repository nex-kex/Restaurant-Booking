from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from users.mixins import StaffRequiredMixin

from .forms import BookingForm, CategoryForm, FeedbackForm, TableForm
from .models import Booking, Category, Feedback, Table


class MainPageTemplateView(TemplateView):
    template_name = "booking/main_page.html"

    # Добавляет форму обратной связи в контекст главной страницы
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_form"] = FeedbackForm()
        return context

    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("booking:main")
        # Если форма невалидна, показываем с ошибками
        context = self.get_context_data()
        context["feedback_form"] = form
        return self.render_to_response(context)


class AboutPageTemplateView(TemplateView):
    template_name = "booking/about.html"


class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    success_url = reverse_lazy("booking:main")
    template_name = "booking/main.html"


class FeedbackDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Feedback


class FeedbackListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Feedback
    paginate_by = 10


class FeedbackChangeStatus(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Feedback
    fields = []
    success_url = reverse_lazy("booking:feedback-list")
    template_name = "booking/feedback_change_status.html"

    def form_valid(self, form):
        current_status = self.object.is_solved
        self.object.is_solved = not current_status
        self.object.save()
        return super().form_valid(form)


class CategoryCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
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
            total_table_count = Table.objects.filter(category=category).count()
            available_table_count = Table.objects.filter(category=category, is_available=True).count()
            categories_with_count.append(
                {
                    "category": category,
                    "available_table_count": available_table_count,
                    "total_table_count": total_table_count,
                }
            )
        context["categories_with_count"] = categories_with_count
        return context

    # Возвращает только те категории, в которых есть доступные для брони столы для обычных пользователй
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            return queryset.filter(tables__is_available=True).distinct()
        else:
            return queryset


class CategoryUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm

    def get_success_url(self):
        return reverse_lazy("booking:category-detail", kwargs={"pk": self.object.pk})


class CategoryDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy("booking:category-list")


class TableCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
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
        if not self.request.user.is_staff:
            return queryset.filter(is_available=True)
        else:
            return queryset


class CategoryTableListView(ListView):
    model = Table

    # Возвращает только доступные столы из определённой категории
    def get_queryset(self):
        category_id = self.kwargs.get("pk")
        queryset = super().get_queryset().filter(category_id=category_id)
        if not self.request.user.is_staff:
            return queryset.filter(is_available=True)
        else:
            return queryset


class TableUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Table
    form_class = TableForm

    def get_success_url(self):
        return reverse_lazy("booking:table-detail", kwargs={"pk": self.object.pk})


class TableDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Table
    success_url = reverse_lazy("booking:table-list")


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm

    def get_success_url(self):
        return reverse_lazy("users:user-detail", kwargs={"pk": self.request.user.pk})

    def form_valid(self, form):
        # Сразу сохраняет пользователя, без необходимости указывать самостоятельно
        booking_instance = form.save(commit=False)
        user = self.request.user
        booking_instance.user = user

        # Проверяем доступность стола
        table = form.cleaned_data.get("table")
        date = form.cleaned_data.get("date")
        duration = form.cleaned_data.get("duration")
        timedelta_duration = timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second)

        start_datetime = date
        end_datetime = start_datetime + timedelta_duration
        print(start_datetime, end_datetime)

        overlapping_bookings = Booking.objects.filter(table=table, status="active").exclude(
            pk=booking_instance.pk if booking_instance.pk else None
        )

        for booking in overlapping_bookings:
            # Получаем время начала и окончания существующей брони
            booking_start = booking.date

            booking_duration = timedelta(
                hours=booking.duration.hour, minutes=booking.duration.minute, seconds=booking.duration.second
            )
            booking_end = booking_start + booking_duration

            # Проверяем пересечение временных интервалов
            if (
                (start_datetime <= booking_start < end_datetime)
                or (start_datetime < booking_end <= end_datetime)
                or (start_datetime <= booking_start <= booking_end <= end_datetime)
            ):
                print(booking_start, booking_end)
                start = timezone.localtime(booking_start).strftime("%H:%M:%S")
                end = timezone.localtime(booking_end).strftime("%H:%M:%S")
                form.add_error("table", f"Этот стол уже забронирован с {start} до {end}")
                return self.form_invalid(form)

        booking_instance.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        seats = form.cleaned_data.get("people")
        table = form.cleaned_data.get("table")

        # Проверяет, чтобы количество людей не превышало число доступных мест
        if seats and table and seats > table.seats:
            form.add_error(
                "table", f"Стол который вы выбрали рассчитан на {table.seats} мест. Выберете другой столик."
            )

        return self.render_to_response(self.get_context_data(form=form))


class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking

    # Запрещает пользователю просматривать чужие бронирования
    def get_object(self, **kwargs):
        user_booking = super().get_object()
        user = self.request.user
        if user != user_booking.user and not self.request.user.is_staff:
            raise PermissionDenied("У вас нет прав для доступа к этой странице.")
        return user_booking


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking

    # Запрещает пользователю просматривать чужие бронирования
    def get_queryset(self, **kwargs):
        user_bookings = super().get_queryset()
        user = self.request.user
        if not self.request.user.is_staff:
            return user_bookings.filter(user=user)
        return user_bookings


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm

    # Запрещает пользователю изменять чужие бронирования
    def get_object(self, **kwargs):
        user_booking = super().get_object()
        user = self.request.user
        if user != user_booking.user and not self.request.user.is_staff:
            raise PermissionDenied("У вас нет прав для доступа к этой странице.")
        return user_booking

    def get_success_url(self):
        return reverse_lazy("booking:booking-detail", kwargs={"pk": self.object.pk})


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking

    def get_success_url(self):
        return reverse_lazy("users:user-detail", kwargs={"pk": self.request.user.pk})

    # Запрещает пользователю удалять чужие бронирования
    def get_object(self, **kwargs):
        user_booking = super().get_object()
        user = self.request.user
        if user != user_booking.user and not self.request.user.is_staff:
            raise PermissionDenied("У вас нет прав для доступа к этой странице.")
        return user_booking
