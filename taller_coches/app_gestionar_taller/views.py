from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
import json

from .models import Cliente, Coche, Servicio, CocheServicio


def menu_principal(request):
    return render(request, 'menuprincipal.html')


def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'lista_clientes.html', {'clientes': clientes})


def lista_coches(request):
    coches = Coche.objects.select_related('cliente').all()
    return render(request, 'lista_coche.html', {'coches': coches})


def lista_servicios(request):
    relaciones = CocheServicio.objects.select_related('servicio', 'coche', 'coche__cliente').all()
    return render(request, 'lista_servicios.html', {'relaciones': relaciones})

def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    coches = Coche.objects.filter(cliente=cliente)
    contexto = {
        'cliente': cliente,
        'coches': coches,
    }
    return render(request, 'detalle_cliente.html', contexto)


def detalle_coche(request, coche_id):
    coche = get_object_or_404(Coche, id=coche_id)

    # Si coche y servicio están relacionados mediante la tabla intermedia CocheServicio
    relaciones = CocheServicio.objects.filter(coche=coche).select_related('servicio')

    contexto = {
        'coche': coche,
        'relaciones_servicio': relaciones,
    }
    return render(request, 'detalle_coche.html', contexto)


def detalle_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)

    # Si coche y servicio están relacionados mediante la tabla intermedia CocheServicio
    relaciones = CocheServicio.objects.filter(servicio=servicio).select_related('coche', 'coche__cliente')

    contexto = {
        'servicio': servicio,
        'relaciones_coche': relaciones,
    }
    return render(request, 'detalle_servicio.html', contexto)


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
            return JsonResponse({
                "id": cliente.id,
                "nombre": cliente.nombre,
                "telefono": cliente.telefono,
                "email": cliente.email
            }, status=201)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Datos inválidos"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def registrar_coche(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cliente = get_object_or_404(Cliente, id=data["cliente_id"])

            coche = Coche.objects.create(
                marca=data["marca"],
                modelo=data["modelo"],
                matricula=data["matricula"],
                cliente=cliente
            )

            return JsonResponse({
                "id": coche.id,
                "marca": coche.marca,
                "modelo": coche.modelo,
                "matricula": coche.matricula,
                "cliente_id": cliente.id
            }, status=201)

        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Datos inválidos"}, status=400)

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

            return JsonResponse({
                "id": servicio.id,
                "nombre": servicio.nombre,
                "descripcion": servicio.descripcion
            }, status=201)

        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Datos inválidos"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def modificar_cliente(request, cliente_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            cliente = get_object_or_404(Cliente, id=cliente_id)

            cliente.nombre = data.get("nombre", cliente.nombre)
            cliente.telefono = data.get("telefono", cliente.telefono)
            cliente.email = data.get("email", cliente.email)
            cliente.save()

            return JsonResponse({
                "id": cliente.id,
                "nombre": cliente.nombre,
                "telefono": cliente.telefono,
                "email": cliente.email
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Datos inválidos"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def modificar_coche(request, coche_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            coche = get_object_or_404(Coche, id=coche_id)

            coche.marca = data.get("marca", coche.marca)
            coche.modelo = data.get("modelo", coche.modelo)
            coche.matricula = data.get("matricula", coche.matricula)

            cliente_id = data.get("cliente_id")
            if cliente_id:
                coche.cliente = get_object_or_404(Cliente, id=cliente_id)

            coche.save()

            return JsonResponse({
                "id": coche.id,
                "marca": coche.marca,
                "modelo": coche.modelo,
                "matricula": coche.matricula,
                "cliente_id": coche.cliente.id
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Datos inválidos"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def modificar_servicio(request, servicio_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            servicio = get_object_or_404(Servicio, id=servicio_id)

            servicio.nombre = data.get("nombre", servicio.nombre)
            servicio.descripcion = data.get("descripcion", servicio.descripcion)
            servicio.save()

            return JsonResponse({
                "id": servicio.id,
                "nombre": servicio.nombre,
                "descripcion": servicio.descripcion
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Datos inválidos"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def eliminar_cliente(request, cliente_id):
    if request.method == "DELETE":
        cliente = get_object_or_404(Cliente, id=cliente_id)
        cliente.delete()
        return JsonResponse({"message": "Cliente eliminado"})

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def eliminar_coche(request, coche_id):
    if request.method == "DELETE":
        coche = get_object_or_404(Coche, id=coche_id)
        coche.delete()
        return JsonResponse({"message": "Coche eliminado"})

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def eliminar_servicio(request, servicio_id):
    if request.method == "DELETE":
        servicio = get_object_or_404(Servicio, id=servicio_id)
        servicio.delete()
        return JsonResponse({"message": "Servicio eliminado"})

    return JsonResponse({"error": "Método no permitido"}, status=405)