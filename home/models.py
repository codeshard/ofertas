from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailadmin.edit_handlers import InlinePanel
from modelcluster.fields import ParentalKey


class HomePageCategories(Orderable, models.Model):
    page = ParentalKey('home.HomePage', related_name='categoria_homepage')
    categoria = models.ForeignKey('anuncios.Categoria',related_name='+')

    class Meta:
        verbose_name = 'Categoría Pagina de Inicio'
        verbose_name_plural = 'Categorías Pagina de Inicio'

    def __str__(self):
        return self.page.title + " -> " + self.categoria.etiqueta

    panels = [
        SnippetChooserPanel('categoria'),
    ]


class HomePage(Page):
    content_panels = Page.content_panels + [
        InlinePanel('categoria_homepage', label=r'Categorías'),
    ]
