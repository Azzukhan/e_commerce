# product_service/urls.py
from django.urls import path
from .views import ProductListCreateView, ProductRetrieveUpdateDestroyView, UpdateInventoryView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('products/<int:pk>/update_inventory/', UpdateInventoryView.as_view(), name='update-inventory'),
]
