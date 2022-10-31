from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, RedirectView
from django.views.generic.edit import FormMixin
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from articleapp.forms import ArticleCreationForm
from articleapp.models import Article, LikeRecord
from articleapp.decorators import article_ownership_required
from commentapp.forms import CommentCreationForm
# Create your views here.


@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleCreationForm
    template_name = 'articleapp/create.html'

    def form_valid(self, form):
        temp_article = form.save(commit=False)
        temp_article.writer = self.request.user
        temp_article.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk':self.object.pk})

@method_decorator(article_ownership_required, 'get')
@method_decorator(article_ownership_required, 'post')
class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleCreationForm
    context_object_name = 'target_article'
    template_name = 'articleapp/update.html'

    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk':self.object.pk})

@method_decorator(article_ownership_required, 'get')
@method_decorator(article_ownership_required, 'post')
class ArticleDelateView(DeleteView):
    model = Article
    context_object_name = 'target_article'
    success_url = reverse_lazy('articleapp:list')
    template_name = 'articleapp/delete.html'


class ArticleDetailView(DetailView, FormMixin):
    model = Article
    form_class = CommentCreationForm
    context_object_name = 'target_article'
    template_name = 'articleapp/detail.html'

class ArticleListView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'articleapp/list.html'
    paginate_by = 25


@transaction.atomic
def db_transaction(user,article):
    if LikeRecord.objects.filter(user=user, article=article).exists():
        raise ValidationError('Like already exists')
    else:
        LikeRecord(user=user, article=article).save()
    article.like += 1
    article.save()



@method_decorator(login_required,'get')
class LikeArticleView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('articleapp:detail', kwargs={'pk':kwargs['pk']})

    def get(self, *args, **kwargs):
        user = self.request.user
        article = get_object_or_404(Article, pk=kwargs['pk'])

        try:
            db_transaction(user,article)
            messages.add_message(self.request, messages.SUCCESS, '좋아요가 반영되었습니다.')
        except ValidationError:
            messages.add_message(self.request, messages.ERROR, '좋아요는 한번만 가능합니다.')
            return HttpResponseRedirect(reverse('articleapp:detail', kwargs={'pk': kwargs['pk']}))

        return super(LikeArticleView, self).get(self.request, *args, **kwargs)