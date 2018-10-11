from django.shortcuts import render

# Create your views here.

def condiciones(request):
	return render(request, 'footer/terminosycondiciones.html', context=None)

def privacidad(request):
	return render(request, 'footer/politicadeprivacidad.html', context=None)

def derechosdeautor(request):
	return render(request, 'footer/derechosdeautor.html', context=None)
def sobre(request):
	return render(request, 'sobre/index.html', context=None)
def blog_de_ayuda(request):
	return render(request, 'sobre/elements.html', context=None)

from django.views.defaults import page_not_found
 
def mi_error_404(request):
    nombre_template = 'footer/404.html'
 
    return render(request, template_name=nombre_template, context = None)