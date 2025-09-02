from django.urls import path

from . import views
from .apps import BookingConfig

app_name = BookingConfig.name

urlpatterns = [
    # Pages
    path("", views.MainPageTemplateView.as_view(), name="main"),
    path("about/", views.AboutPageTemplateView.as_view(), name="about"),
    # Categories
    path("category/", views.CategoryListView.as_view(), name="category-list"),
    path("category/create/", views.CategoryCreateView.as_view(), name="category-create"),
    path("category/<int:pk>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path("category/<int:pk>/update/", views.CategoryUpdateView.as_view(), name="category-update"),
    path("category/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category-delete"),
    # Tables
    path("table/", views.TableListView.as_view(), name="table-list"),
    path("table/create/", views.TableCreateView.as_view(), name="table-create"),
    path("table/<int:pk>/", views.TableDetailView.as_view(), name="table-detail"),
    path("table/<int:pk>/update/", views.TableUpdateView.as_view(), name="table-update"),
    path("table/<int:pk>/delete/", views.TableDeleteView.as_view(), name="table-delete"),
    # Bookings
    path("booking/", views.BookingListView.as_view(), name="booking-list"),
    path("booking/create/", views.BookingCreateView.as_view(), name="booking-create"),
    path("booking/<int:pk>/", views.BookingDetailView.as_view(), name="booking-detail"),
    path("booking/<int:pk>/update/", views.BookingUpdateView.as_view(), name="booking-update"),
    path("booking/<int:pk>/delete/", views.BookingDeleteView.as_view(), name="booking-delete"),
]
