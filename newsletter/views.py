from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Newsletter

# Create your views here.
class NewsletterArchiveView(ListView):
    model = Newsletter
    template_name = 'newsletter/archive.html'
    context_object_name = 'newsletters'
    paginate_by = 5

    def get_queryset(self):
        return Newsletter.objects.filter(is_published=True)


class NewsletterDetailView(DetailView):
    model = Newsletter
    template_name = 'newsletter/detail.html'
    context_object_name = 'newsletter'

    def get_queryset(self):
        # Only published newsletters visible publicly
        return Newsletter.objects.filter(is_published=True)
