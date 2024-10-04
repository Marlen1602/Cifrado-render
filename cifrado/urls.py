from django.urls import path
from . import views

urlpatterns = [
    path('cifrado_cye/', views.cifrado_cye_view, name='cifrado_cye'),  # Ruta para el CifradoCyE
    path('cifrado_ays/', views.cifrado_ays_view, name='cifrado_ays'),  # Ruta para el CifradoAyS
    path('acerca_de/', views.acerca_de_view, name='acerca_de'),  # Ruta para Acerca de
    path('', views.cifrado_cye_view, name='index'),  # Página principal redirige a CifradoCyE
]
