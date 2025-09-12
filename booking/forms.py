from django import forms

from users.mixins import FormControlMixin

from .models import Booking, Category, Feedback, Table


class FeedbackForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = Feedback
        fields = "__all__"
        exclude = ["is_solved"]


class CategoryForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = Category
        fields = "__all__"


class TableForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = Table
        fields = ["seats", "price", "time_open", "time_close", "comment", "is_available", "category"]
        widgets = {"is_available": forms.CheckboxInput()}


class BookingForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = Booking
        fields = "__all__"
        exclude = ["user", "status"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}

    # Сортировка столов для бронирования - выбрать можно только из тех, что доступны
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["table"].queryset = Table.objects.filter(is_available=True)
