from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

# --- Simulación de base de datos local en memoria ---
data_list = []

# Añadiendo datos de ejemplo iniciales
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False})


class DemoRestApi(APIView):
    """
    Vista para listar (GET) y crear (POST) elementos.
    Ruta esperada: /index/
    """
    name = "Demo REST API"

    def get(self, request):
        # Filtra la lista para incluir solo los elementos donde 'is_active' es True
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        # Validación mínima
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos (name, email).'}, status=status.HTTP_400_BAD_REQUEST)

        # Asignación de datos automáticos
        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        
        # Guardado
        data_list.append(data)

        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    """
    Vista para manipular un item específico solicitudes (PUT, PATCH, DELETE).
    Ruta esperada: /<id>/
    """
    name = "Demo REST API Item"

    def get_item(self, item_id):
        # Método auxiliar para busqueda en la lista
        for item in data_list:
            if item['id'] == item_id:
                return item
        return None

    def put(self, request, id):
        item = self.get_item(id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        # PUT reemplaza valores pero manteniendo el ID original
        item['name'] = data.get('name', item['name'])
        item['email'] = data.get('email', item['email'])
        
        return Response({'message': 'Elemento actualizado completamente.', 'data': item}, status=status.HTTP_200_OK)

    def patch(self, request, id):
        item = self.get_item(id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        # PATCH actualiza solo los campos incluidos en la request
        item['name'] = data.get('name', item['name'])
        item['email'] = data.get('email', item['email'])
        item['is_active'] = data.get('is_active', item['is_active'])

        return Response({'message': 'Elemento actualizado parcialmente.', 'data': item}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        item = self.get_item(id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Eliminado lógico
        item['is_active'] = False

        return Response({'message': 'Elemento eliminado lógicamente.'}, status=status.HTTP_204_NO_CONTENT)