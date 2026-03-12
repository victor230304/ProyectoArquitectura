from django.http import JsonResponse
from .models import Cliente,Coche
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Cliente, Coche, Servicio, CocheServicio


def lista_clientes(request):
    clientes = list(Cliente.objects.values("id", "nombre", "telefono", "email"))
    return JsonResponse(clientes, safe=False)

def lista_coches(request):
    coches = list(Coche.objects.values("marca","modelo","matricula"))
    return JsonResponse(coches,safe=False)

def lista_servicios(request):
    servicios = list(Servicio.objects.values("nombre","descripcion"))
    return JsonResponse(servicios,safe=False)
    
def detalle_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.values("id", "nombre", "telefono", "email").get(id=cliente_id)
        return JsonResponse(cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)

@csrf_exempt
def registrar_cliente(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.create(
                nombre=data["nombre"],
                telefono=data["telefono"],
                email=data["email"]
            )
            return JsonResponse({"id": cliente.id, "nombre": cliente.nombre, "telefono": cliente.telefono, "email": cliente.email}, status=201)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Datos inválidos"}, status=400)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def registrar_coche(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cliente_id = data["cliente_id"]
            cliente = Cliente.objects.get(id=cliente_id)
            coche = Coche.objects.create(
                marca=data["marca"],
                modelo=data["modelo"],
                matricula=data["matricula"],
                cliente=cliente
            )
            return JsonResponse({"id": coche.id, "marca": coche.marca, "modelo": coche.modelo, "matricula": coche.matricula, "cliente_id": cliente.id}, status=201)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Datos inválidos"}, status=400)
        except Cliente.DoesNotExist:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def registrar_servicio(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            servicio = Servicio.objects.create(
                nombre=data["nombre"],
                descripcion=data["descripcion"]
            )
            return JsonResponse({"id": servicio.id, "nombre": servicio.nombre, "descripcion": servicio.descripcion}, status=201)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Datos inválidos"}, status=400)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)   
    
@csrf_exempt
def modificar_cliente(request, cliente_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.get(id=cliente_id)
            cliente.nombre = data.get("nombre", cliente.nombre)
            cliente.telefono = data.get("telefono", cliente.telefono)
            cliente.email = data.get("email", cliente.email)
            cliente.save()
            return JsonResponse({"id": cliente.id, "nombre": cliente.nombre, "telefono": cliente.telefono, "email": cliente.email})
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Datos inválidos"}, status=400)
        except Cliente.DoesNotExist:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405
                            )
    
@csrf_exempt
def modificar_coche(request, coche_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            coche = Coche.objects.get(id=coche_id)
            coche.marca = data.get("marca", coche.marca)
            coche.modelo = data.get("modelo", coche.modelo)
            coche.matricula = data.get("matricula", coche.matricula)
            cliente_id = data.get("cliente_id")
            if cliente_id:
                cliente = Cliente.objects.get(id=cliente_id)
                coche.cliente = cliente
            coche.save()
            return JsonResponse({"id": coche.id, "marca": coche.marca, "modelo": coche.modelo, "matricula": coche.matricula, "cliente_id": coche.cliente.id})
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Datos inválidos"}, status=400)
        except Coche.DoesNotExist:
            return JsonResponse({"error": "Coche no encontrado"}, status=404)
        except Cliente.DoesNotExist:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
@csrf_exempt
def eliminar_cliente(request, cliente_id):
    if request.method == "DELETE":
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            cliente.delete()
            return JsonResponse({"message": "Cliente eliminado"})
        except Cliente.DoesNotExist:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
        




