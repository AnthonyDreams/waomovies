from django.http import JsonResponse
from django.contrib import messages

class AjaxFormMixin(object):
	def form_invalid(self, form):
		response = super(AjaxFormMixin, self).form_invalid(form)
		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response

	def form_valid(self, form):
		response = super(AjaxFormMixin, self).form_valid(form)
		if self.request.is_ajax():
			if form.is_valid():
				instance = form.save(commit=False)
				instance.user = self.request.user
				instance.save()
				# message success
					
				data = {
					'message': "Successfully submitted form data."
				}
			return JsonResponse(data)
		else:
			return response

class FavoritosAjaxFormMixin(object):
	def form_invalid(self, form):
		response = super(AjaxFormMixin, self).form_invalid(form)
		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response

	def form_valid(self, form):
		response = super(FavoritosAjaxFormMixin, self).form_valid(form)
		juan = request.user.id
		if self.request.is_ajax():
			if form.is_valid():
				instance = form.save(commit=False)
				instance.favoritos.add(juan)
				instance.pelicula_id = 1
				instance.save()
				# message success
					
				data = {
					'message': "Successfully submitted form data."
				}
			return JsonResponse(data)
		else:
			return response