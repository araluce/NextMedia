# -*- coding: UTF-8 -*-

import os 

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from .forms import *

from pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.test_database

usuarios = db['usuarios']
videos = db['videos']


def index(request):
	if('username' in request.session):
		return render(request, 'index.html', {'form_log' : LoginForm(), 'usuario' : request.session['username'], 'lista_usu' : infousuarios()})
	return render(request, 'index.html', {'form_log' : LoginForm(), 'lista_usu' : infousuarios()})

def login(request):
	if request.method=='POST':
		form_log = LoginForm(request.POST)
		x = db.usuarios.find_one({"Usuario": request.POST['User']})
		if x != None:
			if x[u'Password']== request.POST['Password']:
				request.session['username'] = request.POST['User']
				return render(request, 'index.html', {'form_log' : form_log, 'usuario' : request.session['username'], 'lista_usu' : infousuarios()})
			else:
				return render(request, 'index.html', {'form_log' : form_log, 'alert' : 'Los datos no son correctos', 'lista_usu' : infousuarios()})
		else:
			return render(request, 'index.html', {'form_log' : form_log, 'alert' : 'El usuario ' + request.POST['User'] + ' no existe', 'lista_usu' : infousuarios()})
	if 'username' in request.session:
		return render(request, 'index.html', {'form_log' : LoginForm(), 'usuario' : request.session['username'], 'lista_usu' : infousuarios()})
	return render(request, 'index.html', {'form_log' : LoginForm(), 'lista_usu' : infousuarios()})

def logout(request):
	del request.session['username']
	return render(request, 'index.html', {'form_log' : LoginForm(), 'lista_usu' : infousuarios()})

def registro(request):

	if request.method=='POST':
		form_reg = RegForm(request.POST, request.FILES)
		if form_reg.is_valid():
			x = db.usuarios.find_one({"Usuario": request.POST['User']})
			if x == None:
				request.session["username"] = request.POST['User']
				if request.FILES:
					urlimg = 'media/' + request.POST['User'] + '/fotos/' + request.FILES['I_perfil'].name
					gestor_avatares(request)
				else:
					urlimg = ''
				db.usuarios.insert({
					"Usuario": request.POST['User'],
					"Nombre": request.POST['Nombre'],
					"Apellidos": request.POST['Apellidos'],
					"Email": request.POST['Email'],
					"Dia" : request.POST['Fecha_day'],
					"Mes" : request.POST['Fecha_month'],
					"Anio" : request.POST['Fecha_year'],
					"Password": request.POST['Password'],
					"Direccion": request.POST['Direccion'],
					"Visa": request.POST['Visa'],
					"I_perfil":  urlimg,
				})
				return render(request, 'info.html', {'form_log' : LoginForm(), 'usuario' : request.session['username'], 'lista_usu' : infousuarios(), 'datos' : infousuario(request.session['username'])})
			else:
				return render(request, 'registro.html', {'form_log' : LoginForm(), 'form_reg' : form_reg, 'alert' : 'El usuario que intenta crear ya existe', 'lista_usu' : infousuarios()})
	if 'username' in request.session:
		 return render(request, 'index.html', {'form_log' : LoginForm(), 'usuario' : request.session['username'], 'alert' : 'Ya estas registrado ' + request.session['username'] + '. No hagas trampa =)', 'lista_usu' : infousuarios()})
	return render(request, 'registro.html', {'form_reg' : RegForm(), 'form_log' : LoginForm(), 'lista_usu' : infousuarios()})

def editar(request):
	if 'username' in request.session:
		data = infousuario(request.session['username'])
		if request.method=='POST':
			if request.FILES:
				urlimg = 'media/' + request.session['username'] + '/fotos/' + request.FILES['I_perfil'].name
				gestor_avatares(request)
			else:
				urlimg = data[10]
			db.usuarios.update(
				{"Usuario": data[0]},
				{
					"Usuario": data[0],
					"Nombre": request.POST['Nombre'],
					"Apellidos": request.POST['Apellidos'],
					"Email": data[3],
					"Dia": data[4],
					"Mes": data[5],
					"Anio": data[6],
					"Password": data[7],
					"Direccion": request.POST['Direccion'],
					"Visa": request.POST['Visa'],
					"I_perfil":  urlimg
				}
			)
			return render(request, 'index.html', {'form_log' : LoginForm(), 'usuario' : request.session['username'], 'lista_usu' : infousuarios()})
		else:
			return render(request, 'editar.html', {'form_log' : LoginForm(), 'usuario' : request.session['username'], 'data' : data, 'lista_usu' : infousuarios()})

	return render(request, 'index.html', {'form_log' : LoginForm(), 'lista_usu' : infousuarios()})

def info(request):
	usuario = request.GET.get('u', None)
	if usuario != None:
		x = db.usuarios.find_one({"Usuario": usuario})
		if x != None:
			data = infousuario(usuario)
			if 'username' in request.session:
				return render(request, 'info.html', {'form_log' : LoginForm(), 'usuario' : usuario, 'datos' : data, 'lista_usu' : infousuarios()})
			else:
				return render(request, 'info.html', {'form_log' : LoginForm(), 'datos' : data, 'privacidad' : True, 'lista_usu' : infousuarios()})
	if 'username' in request.session:
		data = infousuario(request.session['username'])
		return render(request, 'info.html', {'form_log' : LoginForm(), 'usuario' : request.session['username'], 'datos' : data, 'lista_usu' : infousuarios()})

	return render(request, 'index.html', {'form_log' : LoginForm(), 'alert' : 'Lo sentimos. No encontramos el usuario que buscas :-(', 'lista_usu' : infousuarios()})

def subir(request):
	if 'username' in request.session:
		if request.method == 'POST':
			form_vid = VideoForm(request.POST, request.FILES)
			urlvid = 'media/' + request.POST['User'] + '/videos/' + request.FILES['video'].name
			gestor_videos(request)
			if form_vid.valid():
				db.usuarios.insert({
					"usuario": request.session['username'],
					"video":  urlvid,
					"titulo": request.POST['titulo'],
					"descripcion": request.POST['descripcion'],
					"Dia" : request.POST['fecha_day'],
					"Mes" : request.POST['fecha_month'],
					"Anio" : request.POST['fecha_year'],
				})
				return render(request, 'index.html', {'form_log' : LoginForm(), 'alert' : 'Su vídeo se ha subido correctamente', 'lista_usu' : infousuarios()})
		else:
			return render(request, 'subir.html', {'form_log' : LoginForm(), 'form_vid' : form_vid , 'usuario' : request.session['username'], 'lista_usu' : infousuarios()})
	return render(request, 'index.html', {'form_log' : LoginForm(), 'alert' : 'Inicia sesión para acceder a esta sección', 'lista_usu' : infousuarios()})
def infousuarios():
	#Buscamos los 10 usuarios con más vídeos subidos
	data = db.usuarios.find({},{"_id" : 0, "Usuario": 1, "I_perfil": 1})[0:10]
	procesa_usu = []
	lista_usu = []
	for doc in data:
		procesa_usu.append(doc)
	for doc in procesa_usu:
		dic = {}
		dic[doc['I_perfil']] = doc['Usuario']
		lista_usu.append(dic)

	return lista_usu
def infousuario(usuario):
	x = db.usuarios.find_one({"Usuario": usuario})
	data = []
	data.append(x[u'Usuario'])
	data.append(x[u'Nombre'])
	data.append(x[u'Apellidos'])
	data.append(x[u'Email'])
	data.append(x[u'Dia'])
	data.append(x[u'Mes'])
	data.append(x[u'Anio'])
	data.append(x[u'Password'])
	data.append(x[u'Direccion'])
	data.append(x[u'Visa'])
	data.append(x[u'I_perfil'])
	return data
def  gestor_avatares( request ):
	directorio = 'NextMedia/static/media/'+ request.session['username']
	directorio_fotos = 'NextMedia/static/media/'+ request.session['username'] + '/fotos/'
	fichero = request.FILES['I_perfil']
	if not os.path.isdir(directorio):
		os.mkdir(directorio)
	if not os.path.isdir(directorio_fotos):
		os.mkdir(directorio_fotos)

	with  open (  directorio_fotos + fichero.name ,  'wb+' )  as  destination :
		for  chunk  in  fichero.chunks ():
			destination.write ( chunk )

def  gestor_videos( request ):
	directorio = 'NextMedia/static/media/'+ request.session['username'] + '/videos/'
	fichero = request.FILES['video']
	if not os.path.isdir(directorio):
		os.mkdir(directorio)
	with  open (  directorio + fichero.name ,  'wb+' )  as  destination :
		for  chunk  in  fichero.chunks ():
			destination.write ( chunk )

@register.filter
def get_item(dictionary, key):
	return dictionary.get(key)