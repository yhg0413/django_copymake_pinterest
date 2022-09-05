from django.shortcuts import render
from django.views.generic import CreateView,UpdateView
from profileapp.models import Profile
from profileapp.forms import ProfileCreationForm
from django.urls import reverse_lazy,reverse
from .decorators import profile_ownership_required
from django.utils.decorators import method_decorator

# Create your views here.



class ProfileCreateView(CreateView):
    model = Profile
    context_object_name = 'traget_profile'
    form_class = ProfileCreationForm
    template_name = 'profileapp/create.html'

    def form_valid(self, form):
        temp_profile = form.save(commit=False)
        temp_profile.user = self.request.user
        temp_profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accountapp:detail',kwargs={'pk': self.object.user.pk})

@method_decorator(profile_ownership_required, 'get')
@method_decorator(profile_ownership_required, 'post')
class ProfileUpdateView(UpdateView):
    model = Profile
    context_object_name = 'traget_profile'
    form_class = ProfileCreationForm
    template_name = 'profileapp/update.html'

    def form_valid(self, form):
        temp_profile = form.save(commit=False)
        temp_profile.user = self.request.user
        temp_profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accountapp:detail',kwargs={'pk': self.object.user.pk})
