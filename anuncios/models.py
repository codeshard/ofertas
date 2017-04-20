# coding=utf-8
#!/usr/bin/env python

import datetime

from django.db import models
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsnippets.models import register_snippet


@register_snippet
class Categoria(Orderable, models.Model):
    etiqueta = models.CharField(max_length=100, db_index=True)
    icono = models.CharField(db_index=True, max_length=100)

    class Meta:
        verbose_name = 'Categoria del Producto'
        verbose_name_plural = 'Categorias de Productos'

    panels = [
        FieldPanel('etiqueta', classname='full'),
        FieldPanel('icono', classname='full'),
        FieldPanel('color', classname="full"),
    ]

    search_fields = [
        index.SearchField('etiqueta', partial_match=True),
    ]

    def __str__(self):
        return self.etiqueta


@register_snippet
class SubCategoria(Orderable, models.Model):
    categoria = models.ForeignKey(Categoria)
    etiqueta = models.CharField(max_length=100, db_index=True)

    class Meta:
        verbose_name = 'SubCategoria del Producto'
        verbose_name_plural = 'SubCategorias de Productos'

    panels = [
        FieldPanel('categoria', classname='full'),
        FieldPanel('etiqueta', classname='full'),
    ]

    search_fields = [
        index.SearchField('etiqueta', partial_match=True),
    ]

    def __str__(self):
        return self.etiqueta


@register_snippet
class TipoMoneda(Orderable, models.Model):
    moneda = models.CharField(db_index=True, max_length=100)

    class Meta:
        verbose_name = 'Tipo de Moneda'
        verbose_name_plural = 'Tipos de Monedas'

    panels = [
        FieldPanel('moneda', classname='full'),
    ]

    search_fields = [
        index.SearchField('moneda', partial_match=True),
    ]

    def __str__(self):
        return self.moneda


@register_snippet
class Provincia(Orderable, models.Model):
    nombre = models.CharField(db_index=True, max_length=100)

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'

    panels = [
        FieldPanel('nombre', classname='full'),
    ]

    search_fields = [
        index.SearchField('nombre', partial_match=True),
    ]

    def __str__(self):
        return self.nombre


@register_snippet
class Municipio(Orderable, models.Model):
    provincia = models.ForeignKey(Provincia)
    nombre = models.CharField(db_index=True, max_length=100)

    class Meta:
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'

    panels = [
        FieldPanel('provincia', classname='full'),
        FieldPanel('nombre', classname='full'),
    ]

    search_fields = [
        index.SearchField('nombre', partial_match=True),
    ]

    def __str__(self):
        return self.nombre


@register_snippet
class Producto(index.Indexed, Orderable, models.Model):
    categoria_producto = models.ForeignKey(SubCategoria)
    precio_producto = models.DecimalField(decimal_places=2, max_digits=6)
    tipo_moneda = models.ForeignKey(TipoMoneda)
    titulo = models.CharField(db_index=True, max_length=250)
    contenido = models.TextField()
    foto = models.FileField(upload_to='productos/fotos/%Y/%m/%d', blank=True)
    #: contacto
    nombre_contacto = models.CharField(db_index=True, max_length=100)
    email_contacto = models.EmailField(blank=True)
    licencia_contacto = models.CharField(blank=True, max_length=100, db_index=True)
    municipio_contacto = models.ForeignKey(Municipio)
    telefono_contacto = models.CharField(db_index=True, max_length=12, blank=True)
    publicado = models.DateTimeField(auto_now_add=True, db_index=True)


    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    panels = [
        FieldPanel('categoria_producto', classname='full'),
        FieldPanel('titulo', classname='full'),
    ]

    search_fields = [
        index.SearchField('titulo', partial_match=True),
        index.FilterField('categoria_producto'),
        index.FilterField('tipo_moneda'),
        index.FilterField('get_municipio_contacto_display'),
    ]

    def __str__(self):
        return self.titulo


class ProductPage(Page):

    def serve(self, request):
        from anuncios.forms import ProductForm

        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                producto = form.save()
                return HttpResponseRedirect('/')
            else:
                print(form.errors)
        else:
            form = ProductForm()
        return render(
            request,
            'crear_anuncio.html',
            {
                'page': self,
                'form': form,
            },
            self.get_context(request)
        )


class ProductListPage(Page):

    def serve(self, request):
        listado_productos = Producto.objects.filter(categoria_producto__etiqueta__iexact=request.GET.get('subcategoria')).all()
        subcategoria = request.GET.get('subcategoria')
        categoria = Categoria.objects.filter(subcategoria__etiqueta=subcategoria).first()
        paginator = Paginator(listado_productos, 25)
        page = request.GET.get('page')
        try:
            productos = paginator.page(page)
        except PageNotAnInteger:
            productos = paginator.page(1)
        except EmptyPage:
            productos = paginator.page(paginator.num_pages)
        print(categoria, subcategoria)
        return render(request, self.template, {'page': self, 'categoria':categoria, 'subcategoria':subcategoria, 'listado_productos': listado_productos, 'productos': productos})


class AnnouncePage(Page):

    def serve(self, request):
        producto = Producto.objects.get(pk=request.GET.get('producto'))
        return render(request, self.template, {'page': self, 'producto':producto})
