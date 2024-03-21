from django.urls import path
from . import views
from django.contrib import admin
from .views import principal

app_name = 'oscar'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Ruta para la página de inicio
    path('login/', views.user_login, name='user_login'),  # Ruta para el inicio de sesión
    path('registro/', views.registro, name='registro'),
    path('principal/', views.principal, name='principal'),
    path('principal/<str:correo>/', principal, name='principal'),
    path('insertar_servicio/', views.insertar_servicio, name='insertar_servicio'),
    path('turnos/', views.turnos_view, name='turnos'),
    path('servicios/', views.servicios_view, name='servicios'),
]

