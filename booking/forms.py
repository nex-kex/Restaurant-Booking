from django import forms

from users.mixins import FormControlMixin

from .models import Booking, Category, Table


class CategoryForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = Category
        fields = "__all__"


class TableForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = Table
        fields = "__all__"


class BookingForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = Booking
        fields = "__all__"
        exclude = ["user", "status"]
