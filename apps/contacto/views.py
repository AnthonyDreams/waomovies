from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
 
def send_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            send_mail(
                data['subject'],
                data['content'],
                'theanthony2d@gmail.com', #FROM
                [data['email']],
                fail_silently=False,
            )
            messages.success(request, 'Gracias por contactarnos, estaremos respondiendo lo más rápido posible.')
            return HttpResponseRedirect('/waomovies/sobre/')
    else:
        form = ContactForm()
 
    return render(request, 'sobre/index.html', {'form': form})
 
def thanks(request):
    return render(request, 'thanks.html')