from django.urls import path
from .views import CompraView

urlpatterns = [
    path('compra/<int:libro_id>/', CompraView.as_view(), name='compra_rapida'),
]