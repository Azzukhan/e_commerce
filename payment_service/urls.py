from django.urls import path
from .views import PaymentCreateView, PaymentDetailView

urlpatterns = [
    path('payments/', PaymentCreateView.as_view(), name='payment-create'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
]
