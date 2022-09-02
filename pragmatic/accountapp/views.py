from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse

# Create your views here.

def hello_world(request):
    return render(request, 'accountapp/hello_world.html')



# Create your models here.

class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/create.html'