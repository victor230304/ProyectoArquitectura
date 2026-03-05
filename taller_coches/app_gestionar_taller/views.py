from django.http import JsonResponse
from .models import Cliente,Coche


def lista_clientes(request):
    clientes = list(Cliente.objects.values("id", "nombre", "telefono", "email"))
    return JsonResponse(clientes, safe=False)

def lista_coches(request):
    coches = list(Coche.objects.values("marca","modelo","matricula"))
    return JsonResponse(coches,safe=False)
    
def detalle_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.values("id", "nombre", "telefono", "email").get(id=cliente_id)
        return JsonResponse(cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)
def detalle_coche(request, coche_id):
    try:
        coche= Coche.objects.values("id","marca","modelo","matricula").get(id=coche_id)
        return JsonResponse(coche)
    except Coche.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)
