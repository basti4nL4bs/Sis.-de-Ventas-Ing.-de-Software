from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.listar_productos, name='listar_productos'),
    path('ventas/registrar/', views.registrar_venta, name='registrar_venta'),
]