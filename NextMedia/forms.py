# -*- coding: UTF-8 -*-
from django import forms
from .models import *

class LoginForm(forms.Form):
	User = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'User', 'class' : 'form-control'}))
	Password = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Password', 'class' : 'form-control', 'type' : 'password'}))

class RegForm(forms.ModelForm):
	class Meta:
		model = Usuario
		widgets = {
			'User' : forms.TextInput(attrs={'placeholder': 'NickName', 'name': 'User', 'class' : 'form-control'}),
			'Nombre' : forms.TextInput(attrs={'placeholder': 'Nombre', 'class' : 'form-control'}),
			'Apellidos' : forms.TextInput(attrs={'placeholder': 'Apellidos', 'class' : 'form-control'}),
			'Email' : forms.TextInput(attrs={'placeholder': 'Email', 'class' : 'form-control'}),
			'Password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class' : 'form-control'}),
			'Visa' : forms.TextInput(attrs={'placeholder': 'VISA', 'class' : 'form-control'}),
			'Fecha' : forms.SelectDateWidget(years=range(1950, 2016), attrs={'class' : 'form-control'}),
			'Direccion' : forms.TextInput(attrs={'placeholder': 'Dirección', 'class' : 'form-control'}),
		}
		fields = ('User', 'Nombre', 'Apellidos', 'Email', 'Password', 'Visa', 'Fecha', 'Direccion', 'I_perfil', 'Aceptacion')

class VideoForm(forms.ModelForm):
	class Meta:
		model = Video
		widgets = {
			'titulo' : forms.TextInput(attrs={'placeholder': 'Título', 'class' : 'form-control'}),
			'descripcion' : forms.Textarea(attrs={'placeholder': 'Introduce alguna descripción', 'class' : 'form-control'}),
		}
		fields = ('video', 'titulo', 'descripcion')