from django.urls import path
from . import views
from .views import (
                    ReviewListCreateView, ReviewsRetrieveUpdateDeleteView,
                )
urlpatterns = [
    path('', views.index, name='index'),
    path('review/', ReviewListCreateView.as_view(),  name='Review-create_api'),
    path('review/<int:pk>/', ReviewsRetrieveUpdateDeleteView.as_view(),  name='Review-update-api'),
]
