from django.test import TestCase
from datetime import datetime

from .models import Usuario
from .forms import RegForm

class ModelosTest(TestCase):
	def test_usuario(self):
		u = Usuario(User = 'usuario', Nombre = 'nombre', Apellidos = 'apellidos', Email = 'email@email.com', Password = 'password', Visa = '5424-8453-7542-8525', Fecha = datetime.now(), Direccion = 'direccion', Aceptacion = 'On' )
		u.save()
		self.assertEqual(u.User, 'usuario')
		print 'Se ha registrado el usuario a traves del modelo con exito'
class FormulariosTest(TestCase):
	def test_registro_usuario(self):
		datos = { 'User' : 'usuario', 'Nombre' : 'nombre', 'Apellidos' : 'apellidos', 'Email' : 'email@email.com', 'Password' : 'password', 'Visa' : '5424-8453-7542-8525', 'Fecha' : datetime.now(), 'Direccion' : 'direccion', 'Aceptacion' : 'On'  }
		form = RegForm(data=datos)
		self.assertTrue(form.is_valid())
		print 'Se ha registrado el usuario a traves del formulario correctamente'