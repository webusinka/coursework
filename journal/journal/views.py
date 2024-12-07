from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import render

def home(request):
    return render(request, 'accounts/home.html')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')