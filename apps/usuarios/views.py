from django.conf import settings
import warnings
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.deprecation import RemovedInDjango21Warning
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render,redirect, render_to_response, get_object_or_404
from django.utils.http import is_safe_url
from django.urls import reverse
from django.contrib.auth import (
	REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
	logout as auth_logout, update_session_auth_hash,
)
from django.views.generic.edit import UpdateView
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect
from django.template.context_processors import csrf

from .forms import *
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Profile
from .models import Usuario
from apps.series.models import Series
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import ( check_password, is_password_usable, make_password,)
from apps.vermas_tarde.models import Vermastarde
from apps.peliculas.models import Peliculas, Generox
from apps.series.models import Series
from django.utils.datastructures import MultiValueDictKeyError
usuario = get_user_model()

@login_required
def user_profile(request):
	user = get_object_or_404(usuario, pk=request.user.id)
	profile = user.profile

	form = Perfil()

	if request.method == 'POST':
		form = Perfil(
			request.POST, request.FILES, instance=request.user.profile)
		if form.is_valid():
			form.save()
			messages.success(request, 'Profile saved successfully!')
			return HttpResponseRedirect(reverse('inicio'))
	else:
		form = Perfil(instance=request.user.profile)

	return render(request, 'profile.html', {'form': form,
														  'profile': profile})







def auths_view(request):
	peliculas = Peliculas.objects.all()
	form = LoginForm(request.POST or None)
	context = {
		"form": form,
		'peliculas':peliculas,

	}
	if request.method =='POST':
		bb = request.POST['email']
		try:
			cc = request.POST['cambiar']
		except MultiValueDictKeyError:
			cc = False
	if form.is_valid():
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		user = authenticate(request, email=email, password=password)
		tt = Usuario.objects.filter(email=email)
		try:
			pwd_valid = Usuario.objects.get(email=email)
		except ObjectDoesNotExist:
			pass
		for i in tt:
			tt = i.active
		if cc and not tt and pwd_valid.check_password(password) :
			if not request.method == 'POST':
				user_change = Usuario.objects.filter(username=tt.username).exists()
				user__ = Usuario.objects.get(username=tt.username)
				if user__.active:
					messages.success(request, "El usuario solicitado ya está validado")
					return HttpResponseRedirect("/waomovies/auth/")	 
				else:
					messages.success(request, "Usuario no existe")
					return HttpResponseRedirect("/waomovies/auth/")
			else: 
				mina = True
				email2 = email
				context = {'min':mina, 'email2':email2,}
				return render(request, "login.html", context)
		if user is not None:
			if not user.last_login:
				login(request, user)
				return HttpResponseRedirect("/waomovies/favoritos/")
			login(request, user)
			

			return HttpResponseRedirect("/waomovies/inicio")
		else:
			useremail = Usuario.objects.filter(email=bb)
			activar_link = False

			try:
				activee = Usuario.objects.get(email=bb)
				
				if useremail.exists():
					error = "La dirección de email y la contraseña no coinciden."
				if not activee.active and pwd_valid.check_password(password):
					error = "Tu cuenta no está activada"
					activar_link = True
				if not useremail.exists():
					error = "Email y contraseña incorrectos, intente de nuevo."
				context = {'error':error, 'activar_link':activar_link,}
				return render(request, "login.html", context)
			except ObjectDoesNotExist:
				
				if useremail.exists():
					error = "La dirección de email y la contraseña no coinciden."
				if not useremail.exists():
					error = "Email y contraseña incorrectos, intente de nuevo."
				context = {'error':error, 'activar_link':activar_link,}
				return render(request, "login.html", context)
	else:
		print("error2")
	return render(request, "login.html", context)

def succes(request):
	context = {

	}

	context['user'] = request.user
	return render(request, "index.html", context)
	
def salir(request):
	logout(request)
	return HttpResponseRedirect(reverse("inicio"))

def cambiar(request):
	logout(request)
	return HttpResponseRedirect(reverse("auth"))


def login_page(request):
	form = LoginForm(request.POST or None)
	context = {
		"form": form
	}
	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None
	if form.is_valid():
		username  = form.cleaned_data.get("username")
		password  = form.cleaned_data.get("password")
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponse("bien")
		else:
			# Return an 'invalid login' error message.
			print("Error")
	return render(request, "login.html", context)


def register_page(request):

	if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('auth'))


	form = RegisterForm(request.POST or None)
	dato = False
	if request.method == 'POST':
		form = RegisterForm(request.POST or None)
		email = request.POST['email']
		username = request.POST['username']
		qz = Usuario.objects.filter(email=email)
		qzz = Usuario.objects.filter(username=username)

		if qz.exists() and qzz.exists():
			dato = "Correo electronico en uso"
			dato2 = "Nombre de usuario en uso"
			return render(request, "registrar.html", {"form": form, "dato":dato, "dato2":dato2,})
		if qz.exists():
			dato = "Correo electronico en uso"
			return render(request, "registrar.html", {"form": form, "dato":dato})

		if qzz.exists():
			dato2 = "Nombre de usuario en uso"
			return render(request, "registrar.html", {"form": form, "dato2":dato2})

		if form.is_valid():
			form.save()
			usera = Usuario.objects.get(email=form.cleaned_data.get("email"))
			if usera.active:

				email = form.cleaned_data.get("email")
				password = form.cleaned_data.get("password1")
				user = authenticate(request, email=email, password=password)
				user = form.save()
				login(request, user)
				messages.success(
						request,
						"Bienvenido " + request.user.full_name + " " + "Prueba añadiendo películas a favorítos, para una mejor selección de tus preferencias:"
					)
				return HttpResponseRedirect(reverse('inicio'))
			else:
				messages.success(
						request,
						"Tu cuenta ha sido creada, por favor verífica tu dirección email."
					)
				error = "Tu cuenta ha sido creada, por favor verífica tu dirección email."
				context = {'error':error}
				return HttpResponseRedirect(reverse('auth'))

	return render(request, "registrar.html", {"form": form, "dato":dato})


class update(UpdateView):
	model = Profile
	fields = ['perfil_img']


def user_detail(request, id, *args, **kwargs):
	usuarioname = usuario.objects.get(username=id)
	usuarioo = usuario.objects.get(id=usuarioname.id)
	comedia = Generox.objects.get(genero_name="comedia")
	accion = Generox.objects.get(genero_name="accion")
	ciencia_ficcion = Generox.objects.get(genero_name="ciencia_ficcion")

	romance = Generox.objects.get(genero_name="romance")

	terror = Generox.objects.get(genero_name="terror")

	fantasia = Generox.objects.get(genero_name="fantasia")

	aventura = Generox.objects.get(genero_name="aventura")

	crimen = Generox.objects.get(genero_name="crimen")
	documental = Generox.objects.get(genero_name="documental")
	suspenso = Generox.objects.get(genero_name="suspenso")
	animacion = Generox.objects.get(genero_name="animacion")
	drama = Generox.objects.get(genero_name="drama")




	if not request.user == usuarioo:
		raise Http404
	user_details = True
	user_favoritos = False
	context = {'usuario':usuarioo,
				'user_details':user_details,
				'user_favoritos':user_favoritos,
				'comedia':comedia,
				'ciencia_ficcion':ciencia_ficcion,
				'terror':terror,
				'romance':romance,
				'aventura':aventura,
				'suspenso':suspenso,
				'documental':documental,
				'crimen':crimen,
				'fantasia':fantasia,
				'animacion':animacion,
				'drama':drama,
				'accion':accion,




	}
	return render(request, 'userprofile.html', context)
from itertools import chain
from datetime import datetime

def user_ver_mas_tarde(request, id, *args, **kwargs):
	usuarioname = usuario.objects.get(username=id)
	usuarioo = usuario.objects.get(id=usuarioname.id)
	if not request.user == usuarioo:
		raise Http404
	user_details = False
	user_favoritos = False
	vermas = True
	peliculas_list = Vermastarde.objects.filter(series_id__isnull=True).filter(usuario_id=usuarioname.id)
	series_list = Vermastarde.objects.filter(series_id__isnull=False).filter(usuario_id=usuarioname.id)

	object_list = Vermastarde.objects.filter(usuario_id=usuarioname.id).order_by("fecha")
	object_listc = Vermastarde.objects.filter(usuario_id=usuarioname.id).count()

	cantidad = object_listc


	peliculasee = Vermastarde.objects.filter(usuario_id=request.user.id)
	peliculase = []

	for i in peliculasee:
		peliculase.append(i.series)
		peliculase.append(i.peliculas)

	paginator = Paginator(object_list, 20)
	page = request.GET.get('page')
	try:
		peliculas = paginator.page(page)
	except PageNotAnInteger:
		peliculas = paginator.page(1)
	except EmptyPage:
		peliculas = paginator.page(paginator.num_pages)
	context = {'usuario':usuarioo,
				'user_details':user_details,
				'peliculas':peliculas,
				'user_favoritos':user_favoritos,
				'cantidad':cantidad,
				'peliculas_list':peliculas_list,
				'series_list':series_list,
				'peliculase':peliculase,
				'vermas':vermas,




	}
	return render(request, 'userprofile.html', context)

def user_ver_favoritos(request, id, *args, **kwargs):
	usuarioname = usuario.objects.get(username=id)

	
	usuarioo = usuario.objects.get(id=usuarioname.id)
	if not request.user == usuarioo:
		raise Http404
	user_details = False
	user_favoritos = True
	peliculas_list = Peliculas.objects.filter(favoritos=usuarioname.id)
	paginator = Paginator(peliculas_list, 20)
	peliculasee = Vermastarde.objects.filter(usuario_id=request.user.id)
	peliculase = []

	for i in peliculasee:
		peliculase.append(i.peliculas)
	page = request.GET.get('page')
	try:
		peliculas = paginator.page(page)
	except PageNotAnInteger:
		peliculas = paginator.page(1)
	except EmptyPage:
		peliculas = paginator.page(paginator.num_pages)
	context = {'usuario':usuarioo,
				'user_details':user_details,
				'peliculas':peliculas,
				'user_favoritos':user_favoritos,
				'peliculas_list':peliculas_list,
				'peliculase':peliculase,



	}
	return render(request, 'userprofile.html', context)

def user_ver_series_favoritos(request, id, *args, **kwargs):
	usuarioname = usuario.objects.get(username=id)

	usuarioo = usuario.objects.get(id=usuarioname.id)
	if not request.user == usuarioo:
		raise Http404
	user_details = False
	user_favoritos = False
	series_fav = True
	peliculasee = Vermastarde.objects.filter(usuario_id=request.user.id)
	peliculase = []

	for i in peliculasee:
		peliculase.append(i.series)
	peliculas_list = Series.objects.filter(favoritos=usuarioname.id)
	paginator = Paginator(peliculas_list, 20)
	page = request.GET.get('page')
	try:
		peliculas = paginator.page(page)
	except PageNotAnInteger:
		peliculas = paginator.page(1)
	except EmptyPage:
		peliculas = paginator.page(paginator.num_pages)
	context = {'usuario':usuarioo,
				'user_details':user_details,
				'peliculas':peliculas,
				'user_favoritos':user_favoritos,
				'peliculas_list':peliculas_list,
				'series_fav':series_fav,
				'peliculase':peliculase,



	}
	return render(request, 'userprofile.html', context)

@login_required
def change_password(request, id):
	user = get_object_or_404(usuario, id=id)
	form = ChangePasswordForm(user)

	if request.method == 'POST':
		form = ChangePasswordForm(user, data=request.POST)
		if form.is_valid():
			if user.check_password(request.POST['old_password']):
				user.set_password(request.POST['new_password1'])
				user.save()
				messages.success(request, "Contraseña cambiada con exito")

				return HttpResponseRedirect(user.get_absolute_url())
				
			else:
				return HttpResponseRedirect(user.get_absolute_url())
				messages.error(request, 'Contraseña incorrecto')

	return render(request, 'userprofile.html', {'form': form})

def profile_edit(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Profile, user_id=request.user)
	juan = request.user
	alber = "/waomovies/usuario/juan"
	form = Perfil(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Foto de perfil cambiada")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.perfil_img,
		"instance": instance,
		"form":form,
	}
	return render(request, "userprofile.html", context)


def user_detail_edit(request, id):
	if not request.user.is_active:
		raise Http404
	



	instance = get_object_or_404(Usuario, id=id)
	juan = request.user
	alber = "/waomovies/usuario/juan"
	form = user_edit(request.POST or None, request.FILES or None, instance=instance)
	if request.method=='POST':
		juana = request.POST['username']
		if juana and not request.POST['email'] and not request.POST['full_name']:
			form = user_username_edit(request.POST or None, request.FILES or None, instance=instance)
			usa = Usuario.objects.filter(username=request.POST['username'])
			if usa.exists():
				messages.info(request, "Nombre de usuario en uso")
				return HttpResponseRedirect(instance.get_absolute_url())
			if " " in juana:
				messages.warning(request, "Nombre de usuario no puede contener espacios")
				return HttpResponseRedirect(instance.get_absolute_url())

			if form.is_valid():
				instance = form.save(commit=False)
				instance.username = request.POST['username']
				instance.save()
				messages.success(request, "Perfil editado")
				return HttpResponseRedirect(instance.get_absolute_url())
		if request.POST['full_name'] and not juana and not request.POST['email']:
			form = full_name_edit(request.POST or None, request.FILES or None, instance=instance)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.full_name = request.POST['full_name']
				instance.save()
				messages.success(request, "Perfil editado")
				return HttpResponseRedirect(instance.get_absolute_url())
		if not request.POST['full_name'] and not juana and  request.POST['email']:
			form = email_edit(request.POST or None, request.FILES or None, instance=instance)
			usa = Usuario.objects.filter(email=request.POST['email'])
			if usa.exists():
				messages.info(request, "Esta dirección de email ya existe")
				return HttpResponseRedirect(instance.get_absolute_url())

			if form.is_valid():
				instance = form.save(commit=False)
				instance.email = request.POST['email']
				instance.save()
				messages.success(request, "Debes confirmar tu dirección email")
				error = "Debes confirmar tu dirección email"
				return HttpResponseRedirect("/waomovies/auth/")
	if form.is_valid():
		instance = form.save(commit=False)
		instance.username = request.POST['username']
		instance.email = request.POST['email']
		instance.full_name = request.POST['full_name']
		instance.save()
		messages.success(request, "Debes confirmar tu dirección email")
		error = "Debes confirmar tu dirección email"
		return HttpResponseRedirect("/waomovies/auth/")

	context = {
		"instance": instance,
		"form":form,
	}
	return render(request, "userprofile.html", context)


def username_detail_edit(request, id, username):
	if not request.user.is_active:
		raise Http404

	

	instance = get_object_or_404(Usuario, username=username)
	juan = request.user
	alber = "/waomovies/usuario/juan"
	form = user_username_edit(request.POST or None, request.FILES or None, instance=instance)
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.username = request.POST['username']
		instance.save()
		messages.success(request, "Perfil editado")
		return HttpResponseRedirect(instance.get_absolute_url())

	else:
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"instance": instance,
		"form":form,
	}

def user_delete(request, id):
	if not request.user.is_active:
		raise Http404
	instance = get_object_or_404(Usuario, id=id)
	instance.delete()
	messages.success(request, "Cuenta Eliminada")
	return HttpResponseRedirect("/waomovies/inicio/")

def activate_user_view(request, code=None, *args, **kwargs):
	if code:
		qs = Profile.objects.filter(activation_key=code)
		if qs.exists() and qs.count() == 1:
			profile = qs.first()
			if not profile.user.active:
				user_ = profile.user
				user_.active = True
				user_.save()
				profile.activation_key=None
				profile.save()
				return redirect("/waomovies/auth/")
	return redirect("/waomovies/auth/")

def reactivate_user_view(request, code=None, *args, **kwargs):
	if code:
		qs = Profile.objects.filter(activation_key=code)
		if qs.exists() and qs.count() == 1:
			profile = qs.first()
			if not profile.user.active:
				user_ = profile.user
				user_.active = True
				user_.save()
				profile.activation_key=None
				profile.save()
				messages.success("Cuenta validada, ahora inicia sesión")
				return redirect("/waomovies/auth/")
	return redirect("/waomovies/auth/")
'''
def change_email_for_validate(request):
	if request.method == 'POST':
		username = request.POST['usernamee']
		user_change = Usuario.objects.filter(username=username).exists()
		user__ = Usuario.objects.get(username=username)
		if user__.active:
			messages.success(request, "El usuario solicitado ya está validado")
			return HttpResponseRedirect("/waomovies/auth/")	 
		else:
			messages.success(request, "Usuario no existe")
			return HttpResponseRedirect("/waomovies/auth/")
	else: 
		mina = True
		context = {'min':mina}
		return render(request, "login.html", context)
'''

def change_email(request):
	if request.method=='POST':
		us = Usuario.objects.get(email=request.POST['old_email'])
		instance = get_object_or_404(Usuario, id=us.id)
		if request.POST['email']:
			form = email_edit(request.POST or None, request.FILES or None, instance=instance)
			usa = Usuario.objects.filter(email=request.POST['email'])
			if usa.exists():
				messages.info(request, "Esta dirección de email ya existe")
				return HttpResponseRedirect(instance.get_absolute_url())

			if form.is_valid():
				instance = form.save(commit=False)
				instance.email = request.POST['email']
				instance.save()
				messages.success(request, "Debes confirmar tu dirección email")
				error = "Debes confirmar tu dirección email"
				return HttpResponseRedirect("/waomovies/auth/")

def favoritos_first(request):
	if request.user.profile.fav_peliculas and request.user.profile.fav_series:
			return HttpResponseRedirect("/waomovies/inicio/")

	peliculas_fav = Peliculas.objects.all().order_by("favoritos")[0:20]
	series_fav = Series.objects.all().order_by("favoritos")[0:20]

	series_fav = Series.objects.all().order_by("favoritos")[0:20]
	count = 8 - request.user.favoritos.all().count()
	count_series = 8 - request.user.favoritos_series.all().count()

	continuar = False
	end = False
	lista = []
	lista2 = []
	for i in peliculas_fav:
		if not i in lista:
			lista.append(i)
	for a in series_fav:
		if not a in lista2:
			lista2.append(a)
	if request.user.favoritos.all().count() >= 8:
			continuar = True
	if request.user.favoritos.all().count() >= 8 and request.method=='POST' and not request.user.profile.fav_peliculas:
		a =Usuario.objects.get(id=request.user.id)
		a.profile.fav_peliculas = True
		a.save()
		return HttpResponseRedirect("/waomovies/favoritos/")
	if request.user.favoritos_series.all().count() >= 8:
		end = True

	if request.user.favoritos_series.all().count() >= 8 and request.method=='POST' and not request.user.profile.fav_series:
		a =Usuario.objects.get(id=request.user.id)
		a.profile.fav_series = True
		a.save()
		return HttpResponseRedirect("/waomovies/inicio/")



	context = {
	'peliculas_fav':lista,
	'series_fav':lista2,
	'continuar':continuar,
	'end':end,
	'count':count,
	'count_series':count_series,


	}

	return render(request, 'favoritos_login.html', context)

@csrf_protect
def password_reset(request,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   extra_context=None,
                   html_email_template_name=None,
                   extra_email_context=None):
    warnings.warn("The password_reset() view is superseded by the "
                  "class-based PasswordResetView().",
                  RemovedInDjango21Warning, stacklevel=2)
    if not request.user.is_authenticated:

        if post_reset_redirect is None:
            post_reset_redirect = reverse('password_reset_done')
        else:
            post_reset_redirect = resolve_url(post_reset_redirect)
        if request.method == "POST":
            emailc = request.POST['email']
            usuario = Usuario.objects.filter(email=emailc)
            if not usuario:
                messages.success(request, "Dirección de email inexistente")
                return HttpResponseRedirect("/reset/password_reset/")
            try:
                usuarios = Usuario.objects.get(email=emailc)
                if not usuarios.active:
                    messages.success(request, "Se ha solicitado el cambio de contraseña de una cuenta no activada")
            except ObjectDoesNotExist:
                pass



            form = password_reset_form(request.POST)
            if form.is_valid():
                opts = {
                    'use_https': request.is_secure(),
                    'token_generator': token_generator,
                    'from_email': from_email,
                    'email_template_name': email_template_name,
                    'subject_template_name': subject_template_name,
                    'request': request,
                    'html_email_template_name': html_email_template_name,
                    'extra_email_context': extra_email_context,
                }
                form.save(**opts)
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = password_reset_form()
        context = {
            'form': form,
            'title': _('Password reset'),
        }
        if extra_context is not None:
            context.update(extra_context)

        return TemplateResponse(request, template_name, context)
    else: 
        return HttpResponseRedirect("/waomovies/inicio/")