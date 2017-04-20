# coding=utf-8
#!/usr/bin/env python

from django import template
from anuncios.models import *

register = template.Library()

@register.assignment_tag
def get_listado_subcategorias(categoria):
    return categoria.subcategoria_set.all(),
