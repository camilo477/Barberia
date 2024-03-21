from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.db import connection
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import ServicioRealizado
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
def user_login(request):
    
    
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        # Verificar si el campo de correo está vacío
        if not correo:
            error_message = "El campo de correo está vacío. Por favor, ingresa tu correo."
            return render(request, 'oscar/user/login.html', {'error_message': error_message})
        
        # Verificar si el campo de contraseña está vacío
        if not password:
            error_message = "El campo de contraseña está vacío. Por favor, ingresa tu contraseña."
            return render(request, 'oscar/user/login.html', {'error_message': error_message})
        
        # Consultar la base de datos para obtener la contraseña correspondiente al correo ingresado
        with connection.cursor() as cursor:
            cursor.execute("SELECT contrasena FROM barberia.empleados WHERE email = %s", [correo])
            row = cursor.fetchone()
        
        # Si se encontró un registro con el correo ingresado
        if row:
            contrasena_db = row[0]
            # Verificar si la contraseña ingresada coincide con la contraseña en la base de datos
            if password == contrasena_db:
                # Usuario autenticado correctamente, redirigir a la página principal con el correo como parámetro en la URL
                return redirect('principal', correo=correo)  # Redirigir a la página deseada con el correo como parámetro
            else:
                # Las contraseñas no coinciden, mostrar un mensaje de error
                error_message = "Contraseña incorrecta. Por favor, inténtalo de nuevo."
                return render(request, 'oscar/user/login.html', {'error_message': error_message})
        else:
            # No se encontró ningún registro con el correo ingresado, mostrar un mensaje de error
            error_message = "Correo no registrado. Por favor, regístrate."
            return render(request, 'oscar/user/login.html', {'error_message': error_message})
    
    return render(request, 'oscar/user/login.html')

def principal(request, correo=None):
    id_empleado = None
    nombre_usuario = None

    if correo:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_empleados, nombre FROM barberia.empleados WHERE email = %s", [correo])
            row = cursor.fetchone()
            if row:
                id_empleado = row[0]
                nombre_usuario = row[1]

    return render(request, 'oscar/principal.html', {'id_empleado': id_empleado, 'nombre_usuario': nombre_usuario, 'correo': correo})


def login_user(request, correo):
    # Simular la autenticación manual
    request.session['logged_in'] = True
    request.session['correo'] = correo

def home(request):
    return render(request, 'home.html')

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario y registrar al usuario en la base de datos
            form.save()
            # Redirigir después del registro exitoso
            return redirect('oscar:user_login')  # Cambiar 'oscar:user_login' por la URL a la que deseas redirigir
    else:
        form = CustomUserCreationForm()
    return render(request, 'oscar/user/registro.html', {'form': form})



def registro(request):
    if request.method == 'POST':
        fecha_contratacion = timezone.now().date()
        
        # Obtener los datos del formulario
        nombre = request.POST.get('nombre')
        contrasena = request.POST.get('contrasena')
        cargo = request.POST.get('cargo')
        correo = request.POST.get('correo')
        
        # Verificar si algún campo está vacío
        if not (nombre and contrasena and cargo and correo):
            error_message = "Todos los campos son requeridos. Por favor, completa todos los campos."
            return render(request, 'oscar/user/registro.html', {'error_message': error_message})
        
        # Insertar los datos en la base de datos
        query = "INSERT INTO empleados (nombre, contrasena, cargo, fecha_contratacion, email) VALUES (%s, %s, %s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, [nombre, contrasena, cargo, fecha_contratacion, correo])
        
        # Redirigir a la página de inicio de sesión
        return redirect('user_login')  # Cambia 'user_login' por la URL de tu vista de inicio de sesión
    
    # Si no es una solicitud POST, mostrar el formulario vacío
    return render(request, 'oscar/user/registro.html')
def lista_tablas(request):
    # Consulta para obtener la lista de tablas en la base de datos
    query = "SHOW TABLES"
    with connection.cursor() as cursor:
        cursor.execute(query)
        database_results = [row[0] for row in cursor.fetchall()]

    return render(request, 'oscar/principal.html', {'database_results': database_results})

from django.http import JsonResponse

def insertar_servicio(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        servicio = request.POST.get('servicio')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        empleado_id = request.user.id  # Suponiendo que el empleado está autenticado y tiene un ID asociado

        # Verificar si algún campo está vacío
        if not (servicio and fecha and hora):
            # Si algún campo está vacío, renderizar la misma página de servicios con un mensaje de error
            error_message = 'Todos los campos son requeridos. Por favor, completa todos los campos.'
            return render(request, 'oscar/servicios.html', {'error_message': error_message})

        # Realizar la inserción en la base de datos utilizando una consulta SQL directa
        query = "INSERT INTO servicios_realizados (empleado_id, tipo_servicio, fecha, hora) VALUES (%s, %s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, [empleado_id, servicio, fecha, hora])

        # Después de procesar los datos, puedes devolver la misma página con un mensaje de éxito si lo deseas
        success_message = 'El servicio se ha insertado correctamente.'
        return render(request, 'oscar/servicios.html', {'success_message': success_message})

    # Si la solicitud no es POST, simplemente renderizar la misma página de servicios sin hacer nada
    return render(request, 'oscar/servicios.html')

def turnos_view(request):
    # Lógica de tu vista de turnos
    return render(request, 'turnos.html')  # Renderiza el template de los turnos

def servicios_view(request):
    # Obtener el nombre y ID del usuario actual del contexto de la plantilla
    nombre_usuario = request.user.username if request.user.is_authenticated else None
    id_empleado = request.user.id if request.user.is_authenticated else None

    # Pasar los datos del usuario al contexto de la plantilla
    return render(request, 'oscar/servicios.html', {'nombre_usuario': nombre_usuario, 'id_empleado': id_empleado})

