from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail
from .utils import code_generator
from django.conf import settings
from django.utils import timezone
from ww import f


class UserManager(BaseUserManager):
	def create_user(self, email, full_name, password=True, is_staff=False,is_admin=False, is_active=False, **extra_fields):
		if not email:
			raise ValueError("El usuario debe tener un dirección de email")
		if not password:
			raise ValueError("El usuario debe tener una contraseña")
		if not full_name:
			raise ValueError("El usuario necesita un nombre")
		user_obj = self.model(
			email = self.normalize_email(email),
			full_name=full_name,
			**extra_fields
			



			)
		user_obj.set_password(password)
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.active = is_active
		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self, full_name, email, password=None, **extra_fields):
		user = self.create_user(
			email,
			full_name,
			password=password,
			is_staff= True, **extra_field)
		return user

	def create_superuser(self, full_name,  email, password=None):
		user = self.create_user(
			email,
			full_name,
			password=password,
			is_staff=True,
			is_admin=True)
		return user

class Usuario(AbstractBaseUser):
	full_name = models.CharField(max_length=30)
	email = models.EmailField(max_length=255, unique=True)
	active = models.BooleanField(default=False)
	staff = models.BooleanField(default=False)
	admin = models.BooleanField(default=False)
	username = models.CharField(max_length=16, null=True, unique=True)
	create_date = models.DateTimeField(auto_now_add=True,blank=True)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = [''] 

	objects = UserManager()

	def __str__(self):
		return self.email

	def get_absolute_url(self):
		return reverse("user_detail", kwargs={"id": self.username})

	def get_full_name(self):
		if self.full_name:
			return self.full_name
		return self.email

	def get_short_name(self):
		return self.email
		
	def has_perm(self, perm, obj=None):
		return True
	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin

	@property
	def is_active(self):
		return self.active
	
# Create your models here.
DEFAULT = 'static/default.png'
class Profile(models.Model):
	user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='profile')
	perfil_img = models.ImageField(upload_to ='static', default='static/default.png', blank=True)
	activation_key	= models.CharField(max_length=120, blank=True, null=True)
	expiration = models.DateTimeField(blank=True, null=True)
	fav_peliculas = models.BooleanField(default=False)
	fav_series = models.BooleanField(default=False)
	codde = models.CharField(max_length=8, blank=True, null=True, unique=True)
	AmiGos = models.ManyToManyField(Usuario, related_name='amigosfor')

	def __str__(self):
		return str(self.user.id)

	@property
	def superamigos(self):
		selfa = self.AmiGos.all()
		amiguitos = Usuario.objects.filter(id__in=selfa)
		username_of_friends = []
		for i in amiguitos:
			username_of_friends.append(i.username)
		return self.user.username
	def get_absolute_url(self):
		return reverse("user_detail", kwargs={"id": self.user.username})
	
	def send_activation_email(self):
		if not self.user.active:
			self.activation_key = code_generator()# 'somekey' #gen key
			self.save()
			#path_ = reverse()

			path_ = reverse('activate', kwargs={"code": self.activation_key})
			subject = 'Activate Account'
			from_email = settings.EMAIL_HOST_USER
			message = f('Activate your account here: {path_}')
			recipient_list = [self.user.email]
			html_message = f('<p>Activate your account here: {path_}</p>')
			print(html_message)
			sent_mail = send_mail(
							subject, 
							message, 
							from_email, 
							recipient_list, 
							fail_silently=False, 
							html_message=html_message)
			sent_mail = False
			return sent_mail
@receiver(post_save, sender=Usuario)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=Usuario)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


class UserPreference(models.Model):
	user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='preference')
	week_recomendation = models.ManyToManyField(settings.MOVIES_DEL_WEB,blank=True, related_name='week_recomendation')
	expired = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)


@receiver(post_save, sender=Usuario)
def create_user_UserPreference(sender, instance, created, **kwargs):
	if created:
		UserPreference.objects.create(user=instance)

@receiver(post_save, sender=Usuario)
def save_user_UserPreference(sender, instance, **kwargs):
	instance.profile.save()
