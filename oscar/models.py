from django.db import models
from django.db import models

class ServicioRealizado(models.Model):
    empleado_id = models.IntegerField()
    tipo_servicio = models.CharField(max_length=255)
    fecha = models.DateField()
    hora = models.TimeField()
    
class empleados(models.Model):
    nombre = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255)
    fecha_contratacion = models.DateField(auto_now_add=True)
    contraseña = models.CharField(max_length=255)