from django.urls import path

from tienda_app.api.views import CompraAPIView

from .views import CompraView

urlpatterns = [
    path('compra/<int:libro_id>/', CompraView.as_view(), name='compra_rapida'),
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
]