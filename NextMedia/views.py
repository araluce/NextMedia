# -*- coding: UTF-8 -*-

import os 
import time

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import *

try:
	from django.utils import simplejson as json
except ImportError:
	import json


from pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.test_database

usuarios = db['usuarios']
videos = db['videos']

def index(request):
	if 'username' in request.session:
		return render(request, 'index.html', {'form_log' : LoginForm(), 'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp(), 'datos' : videos_todos()})
	return HttpResponseRedirect("/registro")

def login(request):
	if request.method=='POST':
		form_log = LoginForm(request.POST)
		x = db.usuarios.find_one({"Usuario": request.POST['User']})
		if x != None:
			if x[u'Password'] == request.POST['Password']:
				request.session['username'] = request.POST['User']
				return HttpResponseRedirect("/subir")
			else:
				return render(request, 'registro.html', {'form_log' : form_log, 'alert' : 'Los datos no son correctos', 'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp()})
		else:
			return render(request, 'registro.html', {'form_log' : form_log, 'alert' : 'El usuario ' + request.POST['User'] + ' no existe', 'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp()})
	return HttpResponseRedirect("/registro")

def logout(request):
	if 'username' in request.session:
		del request.session['username']
	return HttpResponseRedirect("/registro")

def registro(request):
	if request.method=='POST':
		form_reg = RegForm(request.POST, request.FILES)
		if form_reg.is_valid():
			x = db.usuarios.find_one({"Usuario": request.POST['User']})
			if x == None:
				request.session["username"] = request.POST['User']
				#contador_visitas[request.POST['User']] = 0
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
					"Visitas" : 0
				})
				return render(request, 'info.html', {'form_log' : LoginForm(), 'lista_usu' : infousuarios(), 'datos' : infousuario(request.session['username']), 'lista_usu_comp' : infousuarios_comp()})
			else:
				return render(request, 'registro.html', {'form_log' : LoginForm(), 'form_reg' : form_reg, 'alert' : 'El usuario que intenta crear ya existe', 'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp()})
	if 'username' in request.session:
		 return HttpResponseRedirect("/subir")
	return render(request, 'registro.html', {'form_reg' : RegForm(), 'form_log' : LoginForm(), 'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp()})

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
					"I_perfil":  urlimg,
					"Visitas" : data[11]
				}
			)
			return HttpResponseRedirect("/info?u="+request.session['username'])
		else:
			return render(request, 'editar.html', {'form_log' : LoginForm(), 'data' : data, 'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp()})

	return HttpResponseRedirect("/registro")

def info(request):
	usuario = request.GET.get('u', None)
	if usuario != None:
		x = db.usuarios.find_one({"Usuario": usuario})
		if x != None:
			data = infousuario(usuario)
			if 'username' in request.session and usuario == request.session['username']:
				return render(request, 'info.html', {'form_log' : LoginForm(), 'datos' : data, 'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp()})
			
			else:
				if 'username' in request.session:
					sube_visita(usuario)
			return render(request, 'info.html', {'form_log' : LoginForm(), 'datos' : data, 'privacidad' : True, 'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp()})
	return render(request, 'registro.html', {'form_log' : LoginForm(), 'alert' : 'Lo sentimos. No encontramos el usuario que buscas :-(', 'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp()})

def sube_visita(usuario):
	data = infousuario(usuario)
	db.usuarios.update(
		{"Usuario": usuario},
		{
			"Usuario": data[0],
			"Nombre": data[1],
			"Apellidos": data[2],
			"Email": data[3],
			"Dia": data[4],
			"Mes": data[5],
			"Anio": data[6],
			"Password": data[7],
			"Direccion": data[8],
			"Visa": data[9],
			"I_perfil":  data[10],
			"Visitas" : int(data[11])+1
		}
	)
def subir(request):
	visitas_usuarios(request)
	if 'username' in request.session:
		if request.method == 'POST':
			form_vid = VideoForm(request.POST, request.FILES)
			urlvid = 'media/' + request.session['username'] + '/videos/' + request.FILES['video'].name
			gestor_videos(request)
			if form_vid.is_valid():
				db.videos.insert({
					"usuario": request.session['username'],
					"video":  urlvid,
					"titulo": request.POST['titulo'],
					"descripcion": request.POST['descripcion'],
					"Fecha" : time.strftime("%x"),
					'Likes' : 0,
					'Dislikes' : 0
				})
				return render(request, 'subir.html', {'form_log' : LoginForm(), 'form_vid' : VideoForm(), 'alert' : 'Su vídeo se ha subido correctamente', 'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp()})
		else:
			return render(request, 'subir.html', {'form_log' : LoginForm(), 'form_vid' : VideoForm(), 'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp()})
	return render(request, 'index.html', {'form_log' : LoginForm(), 'alert' : 'Inicia sesión para acceder a esta sección', 'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp()})
def directorio(request):
	usuario = request.GET.get('u', None)
	if usuario != None:
		x = db.usuarios.find({},{"_id" : 0, "usuario": 1})
		if x != None:
			data = videos(usuario)
			return render(request, 'directorio.html', {'usuario' : usuario, 'form_log' : LoginForm(), 'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp(), 'datos' : data})
	if 'username' in request.session:
		data = videos(request.session['username'])
		return render(request, 'directorio.html', {'usuario' : request.session['username'], 'form_log' : LoginForm(), 'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp(), 'datos' : data})
	return render(request, 'registro.html', {'form_log' : LoginForm(), 'alert' : 'El usuario que busca no existe', 'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp()})
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
def infousuarios_comp():
	data = db.usuarios.find({},{"_id" : 0, "Usuario": 1, "I_perfil": 1})
	procesa_usu = []
	lista_usu = []
	for doc in data:
		procesa_usu.append(doc)
	for doc in procesa_usu:
		dic = {}
		dic[doc['I_perfil']] = doc['Usuario']
		lista_usu.append(dic)
	return lista_usu
def videos(usuario):
	x = db.videos.find({'usuario' : usuario},{"_id" : 0, "usuario": 1, "video" : 1, "titulo" : 1, "descripcion" : 1, "Fecha" : 1, "Likes" : 1, "Dislikes" : 1})
	datos_finales = []
	for doc in x:
		datos_finales.append(doc)
	return datos_finales

def videos_todos():
	x = db.videos.find({},{"_id" : 0, "usuario": 1, "video" : 1, "titulo" : 1, "descripcion" : 1, "Fecha" : 1, "Likes" : 1, "Dislikes" : 1})
	datos_finales = []
	for doc in x:
		datos_finales.append(doc)
	print datos_finales
	return datos_finales

def info_videos(video):
	x = db.videos.find_one({'video' : video})
	datos_finales = []
	datos_finales.append(x[u'usuario'])
	datos_finales.append(x[u'video'])
	datos_finales.append(x[u'titulo'])
	datos_finales.append(x[u'descripcion'])
	datos_finales.append(x[u'Fecha'])
	datos_finales.append(x[u'Likes'])
	datos_finales.append(x[u'Dislikes'])
	return datos_finales

def contador_videos(usuario):
	x = db.videos.find({'usuario' : usuario},{"_id" : 0})
	contador = 0
	for doc in x:
		contador += 1
	return contador

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
	data.append(x[u'Visitas'])
	data.append(contador_videos(usuario))
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

def like_video(request):
	if request.method == 'POST':
		user = request.user
		v = request.POST['slug']
		video = db.videos.find_one({'video' : v})
		if video != None:
			datos = info_videos(v)
			datos[5] = int(datos[5])+1
			db.videos.update(
				{"video": v},
				{
					"usuario": datos[0],
					"video": datos[1],
					"titulo": datos[2],
					"descripcion": datos[3],
					"Fecha": datos[4],
					"Likes": datos[5],
					"Dislikes": datos[6],
				}
			)
			
			message = 'You liked this'

			ctx = {'likes_count': datos[5], 'message': message, 'video' : datos[1]}
			# use mimetype instead of content_type if django < 5
			return HttpResponse(json.dumps(ctx), content_type='application/json')

def dislike_video(request):
	if request.method == 'POST':
		user = request.user
		v = request.POST['dislk']
		video = db.videos.find_one({'video' : v})
		if video != None:
			datos = info_videos(v)
			datos[6] = int(datos[6])+1
			db.videos.update(
				{"video": v},
				{
					"usuario": datos[0],
					"video": datos[1],
					"titulo": datos[2],
					"descripcion": datos[3],
					"Fecha": datos[4],
					"Likes": datos[5],
					"Dislikes": datos[6],
				}
			)
			
			message = 'You liked this'

			ctx = {'dislikes_count': datos[6], 'message': message, 'video' : datos[1]}
			# use mimetype instead of content_type if django < 5
			return HttpResponse(json.dumps(ctx), content_type='application/json')
def visitas_usuarios(request):
	params = request.GET
	usuarios = db.usuarios.find({},{"_id":0, "Usuario": 1, "Visitas": 1})
	datos={}
	datos[0]=list()
	datos[1]=list()
	for x in usuarios:
		datos[0].append(x[u'Usuario'])
		datos[1].append(x[u'Visitas'])
	return JsonResponse(datos, safe=False)

def likes_videos(request):
	params = request.GET
	usuarios = db.videos.find({},{"_id":0, "titulo": 1, "Likes": 1})
	datos={}
	datos[0]=list()
	datos[1]=list()
	for x in usuarios:
		datos[0].append(x[u'titulo'])
		datos[1].append(x[u'Likes'])
	return JsonResponse(datos, safe=False)

def dislikes_videos(request):
	params = request.GET
	usuarios = db.videos.find({},{"_id":0, "titulo": 1, "Dislikes": 1})
	datos={}
	datos[0]=list()
	datos[1]=list()
	for x in usuarios:
		datos[0].append(x[u'titulo'])
		datos[1].append(x[u'Dislikes'])
	return JsonResponse(datos, safe=False)

def estadisticas (request):
	return render(request, 'estadisticas.html', {'form_log' : LoginForm(),'lista_usu' : infousuarios(), 'lista_usu_comp' : infousuarios_comp()})

@register.filter
def get_item(dictionary, key):
	return dictionary.get(key)