from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseForbidden

from django.views.generic import CreateView,DetailView,UpdateView,DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse

from articleapp.models import Article
from .forms import AccountUpdateForm
from .decorators import account_ownership_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import MultipleObjectMixin

has_ownership = [
    account_ownership_required,login_required
]


# Create your views here.


# Create your models here.

class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'accountapp/create.html'


@method_decorator(has_ownership, 'get')
class AccountDetailView(DetailView,MultipleObjectMixin):
    model = User
    template_name = 'accountapp/detail.html'
    context_object_name = "target_user"

    paginate_by = 25

    def get_context_data(self, **kwargs):
        object_list = Article.objects.filter(
            writer = self.get_object()
        )
        return super(AccountDetailView, self).get_context_data(object_list=object_list, **kwargs)

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = "target_user"
    template_name ='accountapp/delete.html'


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountUpdateView(UpdateView):
    model = User
    form_class = AccountUpdateForm
    success_url = reverse_lazy('home')
    template_name = 'accountapp/update.html'
    context_object_name = "target_user"

    """
    인증 코드
    """

    # def get(self, *args, **kwargs):
    #     if self.request.user.is_authenticated and self.get_object() == self.request.user:
    #         return super().get(*args, **kwargs)
    #     else:
    #         return HttpResponseForbidden()
    #
    # def post(self, *args, **kwargs):
    #     if self.request.user.is_authenticated and self.get_object() == self.request.user:
    #         return super().get(*args, **kwargs)
    #     else:
    #         return HttpResponseForbidden()