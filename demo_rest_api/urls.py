from django.urls import path
from . import views

urlpatterns = [
   # Ruta para GET para visualizar lista y POST para crear
   path("index/", views.DemoRestApi.as_view(), name="demo_rest_api_resources"),
   
   # Ruta para PUT, PATCH, DELETE, para esto es necesario el uso del ID
   path("<str:id>/", views.DemoRestApiItem.as_view(), name="demo_rest_api_item_resources"),
]