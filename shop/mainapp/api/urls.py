from django.urls import path

from .api_views import (
    CategoryAPIView,
    SmartphoneListAPIView,
    NotebookListAPIView,
    SmartphoneRetrieveAPIView
)

urlpatterns = [
    path('categories/<str:id>/', CategoryAPIView.as_view(), name='categories_list'),
    path('smartphones/', SmartphoneListAPIView.as_view(), name='smartphones'),
    path('smartphones/<str:id>/', SmartphoneRetrieveAPIView.as_view(), name='category_detail'),
    path('notebooks/', NotebookListAPIView.as_view(), name='notebooks')
]