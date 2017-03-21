# coding: utf-8

from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel,
)

from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

class HomePage(Page):
    pass



class Pictograma(models.Model):
    """

    """
    nombre = models.CharField("Nombre del picto", max_length=254, blank=True)
    picto = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Picto'
    )
    descripcion = models.TextField(
    	help_text="descripción del picto",
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
        FieldPanel('descripcion'),
    ]

class Linea(models.Model):
	pass


class Pagina(Page):
	titulo = models.CharField("Título de la página", max_length=254, blank=True)
	linea = Linea()