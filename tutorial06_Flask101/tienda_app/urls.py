from django.urls import path
from tienda_app.api.views import CompraAPIView, ProductosAPIView
from .views import CompraView

urlpatterns = [
    path('compra/<int:libro_id>/', CompraView.as_view(), name='compra_rapida'),
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
    path('api/v1/productos/', ProductosAPIView.as_view(), name='api_productos'),
]