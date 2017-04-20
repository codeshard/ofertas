# coding=utf-8
#!/usr/bin/env python

from django import forms
from crispy_forms.bootstrap import InlineRadios, FormActions, InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, Button

from captcha.fields import CaptchaField
from .models import Producto, Categoria, SubCategoria, Provincia, Municipio


class ProductForm(forms.ModelForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_class = 'ad-form form-opt'
        self.helper.form_name = 'ad_form'
        self.helper.form_id = 'ad_form'
        self.helper.layout = Layout(
            Div(
                Field(
                    'categoria_producto',
                    css_class='chosen-select',
                ),
                css_class='cl-xs-12 col-sm-12'
            ),
            Div(
                Div(
                    Field(
                        'precio_producto',
                        css_class='onlyFloats'
                    ),
                    css_class='cl-xs-12 col-sm-2'
                ),
                Div(
                    Field(
                        'tipo_moneda',
                    ),
                    css_class='cl-xs-12 col-sm-2'
                ),
                Div(
                    Field(
                        'titulo'
                    ),
                    css_class='cl-xs-12 col-sm-8'
                )
            ),
            Div(
                Div(
                    Field(
                        'contenido'
                    )
                ),
                css_class='cl-xs-12 col-lg-12 col-sm-4'
            ),
            Div(
                Div(
                    Field(
                        'foto'
                    )
                ),
                css_class='cl-xs-12 col-lg-12 col-sm-4'
            ),
            Div(
                Div(
                    Field(
                        'nombre_contacto'
                    ),
                    css_class='cl-xs-12 col-sm-4'
                ),
                Div(
                    Field(
                        'email_contacto'
                    ),
                    css_class='cl-xs-12 col-sm-4'
                ),
                Div(
                    Field(
                        'licencia_contacto'
                    ),
                    css_class='cl-xs-12 col-sm-4'
                ),
            ),
            Div(
                Div(
                    Field(
                        'municipio_contacto'
                    ),
                    css_class='cl-xs-12 col-sm-6'
                ),
                Div(
                    Field(
                        'telefono_contacto'
                    ),
                    css_class='cl-xs-12 col-sm-6'
                )
            ),
            Div(
                Div(
                    Field(
                        'captcha'
                    ),
                    css_class='cl-xs-12 col-sm-4'
                ),
            ),
            
        )
        self.fields['categoria_producto'].label = r'Categoría:'
        self.fields['categoria_producto'].empty_label = r'Por favor, seleccione'
        self.fields['categoria_producto'].choices = categories_as_choices()
        self.fields['categoria_producto'].widget.attrs = {'required': ''}
        self.fields['precio_producto'].label = r'Precio:'
        self.fields['tipo_moneda'].label = r' '
        self.fields['tipo_moneda'].empty_label = None
        self.fields['contenido'].widget.attrs = {'rows': '7'}
        self.fields['municipio_contacto'].choices = municipios_as_choices()

    class Meta:
        model = Producto
        fields = '__all__'

def categories_as_choices():
    categories = []
    for category in Categoria.objects.all():
        new_category = []
        sub_categories = []
        for sub_category in category.subcategoria_set.all():
            sub_categories.append([sub_category.id, sub_category.etiqueta])
        new_category = [category.etiqueta, sub_categories]
        categories.append(new_category)
    return categories

def municipios_as_choices():
    municipios = []
    for provincia in Provincia.objects.all():
        new_provincia = []
        new_municipios = []
        for municipio in provincia.municipio_set.all():
            new_municipios.append([municipio.id, municipio.nombre])
        new_provincia = [provincia.nombre, new_municipios]
        municipios.append(new_provincia)
    return municipios
