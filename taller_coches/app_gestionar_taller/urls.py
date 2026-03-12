from django.urls import path
from .views import (
    menu_principal,
    lista_clientes,
    detalle_cliente,
    lista_coches,
    detalle_coche,
    lista_servicios,
    detalle_servicio,
    registrar_cliente,
    registrar_coche,
    registrar_servicio,
    modificar_cliente,
    modificar_coche,
    modificar_servicio,
    eliminar_cliente,
    eliminar_coche,
    eliminar_servicio,
)

urlpatterns = [
    path('menu/', menu_principal, name='menu_principal'),

    path('clientes/', lista_clientes, name='lista_clientes'),
    path('clientes/<int:cliente_id>/', detalle_cliente, name='detalle_cliente'),
    path('clientes/registrar/', registrar_cliente, name='registrar_cliente'),
    path('clientes/modificar/<int:cliente_id>/', modificar_cliente, name='modificar_cliente'),
    path('clientes/eliminar/<int:cliente_id>/', eliminar_cliente, name='eliminar_cliente'),

    path('coches/', lista_coches, name='lista_coches'),
    path('coches/<int:coche_id>/', detalle_coche, name='detalle_coche'),
    path('coches/registrar/', registrar_coche, name='registrar_coche'),
    path('coches/modificar/<int:coche_id>/', modificar_coche, name='modificar_coche'),
    path('coches/eliminar/<int:coche_id>/', eliminar_coche, name='eliminar_coche'),

    path('servicios/', lista_servicios, name='lista_servicios'),
    path('servicios/<int:servicio_id>/', detalle_servicio, name='detalle_servicio'),
    path('servicios/registrar/', registrar_servicio, name='registrar_servicio'),
    path('servicios/modificar/<int:servicio_id>/', modificar_servicio, name='modificar_servicio'),
    path('servicios/eliminar/<int:servicio_id>/', eliminar_servicio, name='eliminar_servicio'),
]