from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth import get_user_model
from .models import Profile
import re
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ValidationError
from django.utils.html import escape
from datetime import datetime
from . import models
import unicodedata


from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _
Usuario = get_user_model()


class RegisterForm(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

	class Meta:
		model = Usuario
		fields = ('email', 'full_name', 'username')

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = Usuario.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError("El email ya existe")
		return email
	def clean_username(self):
		username = self.cleaned_data.get('username')
		us = Usuario.objects.filter(username=username)
		if us.exists():
			raise forms.ValidationError('El nombre de usuario ya existe')
		return username

		if username in ['@, #, $, ^, /, *, (, ). -, ., ñ, Ñ, ;, ., :, |, !,¡, ?, =,¿ ']:
			raise ValidationError('El nombre de usuario no puede contener los siguientes caracteres:' + '@, #, $, ^, /, *, (, ). -, ., ñ, Ñ, ;, ., :, |, !,¡, ?, =,¿ ')

		if len(username) <= 4:
			raise ValidationError('El nombre de usuario debe tener más de cuatro caracteres')

		if len(username) >= 16:
			raise ValidationError('El nombre de usuario debe tener menos de 16 caracteres de cuatro caracteres')

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(RegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.active = False # send confirmation email
		if commit:
			user.save()
			user.profile.send_activation_email()
		return user



class UserAdminCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = Usuario
		fields = ('email', 'full_name','username')

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserAdminCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserAdminChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = Usuario
		fields = ('full_name','email', 'password', 'active', 'admin')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]



class LoginForm(forms.Form):
	email = forms.CharField(label='email')
	password = forms.CharField(widget=forms.PasswordInput)

class Perfil(forms.ModelForm):

	class Meta:
		model = Profile
		fields = [
			'perfil_img',
		
		]

	def clean(data):
		cleaned_data = super().clean()

class ChangePasswordForm(PasswordChangeForm):

	def clean(self):
		old_password = self.data.get('old_password')
		new_password = self.data.get('new_password1')
		confirm_new_password = self.data.get('new_password2')


		if not re.search('[0-9]+', new_password):
			raise ValidationError(
				'Tu contraseña debe contener al menos un numero')

		if len(new_password) < 8:
			raise ValidationError('Tu contraseña debe ser mayor de 8 caracteres')

		if len(new_password) > 20:
			raise ValidationError('Tu contraseña debe ser menor de 20 caracteres')

		if old_password == new_password:
			raise ValidationError(
				'Tu nueva contraseña no puede ser igual a tu vieja contraseña')


class user_edit(forms.ModelForm):
	username = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	full_name = forms.CharField(required=False)

	class Meta:
		model = Usuario
		fields = ('username', 'email', 'full_name')

	def clean_email(self):
		username = self.cleaned_data.get('username')
		email = self.cleaned_data.get('email')

		if email and Usuario.objects.filter(email=email).exclude(username=username).count():
			raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
		return email

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(user_edit, self).save(commit=False)
		user.active = False # send confirmation email
		if not commit:
			user.save()
			user.profile.send_activation_email()
		return user

class user_username_edit(forms.ModelForm):
	username = forms.CharField(required=True)

	class Meta:
		model = Usuario
		fields = ('username',)

	def clean_email(self):
		username = self.cleaned_data.get('username')
		if username and Usuario.objects.filter(username=username).count():
			raise forms.ValidationError('This username is already in use. Please supply a different email address.')
		return username

class full_name_edit(forms.ModelForm):
	full_name = forms.CharField(required=True)

	class Meta:
		model = Usuario
		fields = ('full_name',)

	def clean_email(self):
		username = self.cleaned_data.get('full_name')

class email_edit(forms.ModelForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = Usuario
		fields = ('email',)

	def clean_email(self):
		email = self.cleaned_data.get('email')

		if email and Usuario.objects.filter(email=email).count():
			raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
		return email
	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(email_edit, self).save(commit=False)
		user.active = False # send confirmation email
		if not commit:
			user.save()
			user.profile.send_activation_email()
		return user
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_email_field_name(): email,
            'active': True,
        })
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            if extra_email_context is not None:
                context.update(extra_email_context)
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                email, html_email_template_name=html_email_template_name,
            )