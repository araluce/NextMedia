# -*- coding: UTF-8 -*-
"""
--------------------------------------------------------------------------------
IV - Infraestructuras Virtuales
DAI - Desarrollo de Aplicaciones para Internet

Grado en Ingeniería Informática (UGR)

Proyecto Final: NextMedia

2016 - Álvaro Fernández-Alonso Araluce
--------------------------------------------------------------------------------

Definiciones de los modelos Usuario y Video

--------------------------------------------------------------------------------
"""

from django.db import models
from django.core.validators import RegexValidator
from django.core.files.storage import FileSystemStorage
from datetime import datetime


class Usuario(models.Model):
	User = models.CharField(max_length=20)
	Nombre = models.CharField(max_length=30)
	Apellidos = models.CharField(max_length=30)
	Email = models.EmailField()
	Password = models.CharField(max_length=15)
	Visa = models.CharField(max_length=19, validators=[RegexValidator(regex='(((\d{4}-){3})|((\d{4} ){3}))\d{4}', message='Formato de Visa inválido', code='nomatch')])
	Fecha = models.DateField()
	Direccion = models.CharField(max_length=50)
	Aceptacion = models.BooleanField()
	I_perfil = models.FileField(blank=True, upload_to='media/fotos')

	def __str__(self):
		return self.User

class Video(models.Model):
	video = models.FileField(blank=True, upload_to='media/fotos')
	titulo = models.CharField(max_length=40)
	descripcion = models.TextField(max_length=300)
	fecha = models.DateTimeField(default=datetime.now(), blank=True)
