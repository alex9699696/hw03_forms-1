from django.shortcuts import render
from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'

    def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        return render('about/author.html')#, context)

class AboutTechView(TemplateView):
    template_name = 'about/tech.html'

    def get_context_data(self, **kwargs):
        #ontext = super().get_context_data(**kwargs)
        return render('about/author.html')#, context)