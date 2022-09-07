from django.urls import path

from subscribeapp.views import SubscriptionView, SubcriptionListView

app_name = 'subscribeapp'

urlpatterns = [
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),
    path('list/',SubcriptionListView.as_view(), name='list'),
]