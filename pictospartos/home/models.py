# coding: utf-8

from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel,
)

from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.wagtailimages.models import Image

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

class Seccion (Page):
    pass


class Pagina(Page):
	titulo = models.CharField("Título de la página", max_length=254, blank=True)
	linea = Linea()


from wagtail.wagtailimages.models import Image

class ListadoDeImagenes(Page):
    titulo = models.CharField("Título de la página", max_length=254, blank=True)

    def get_context(self, request):
        # Get the full unpaginated listing of resource pages as a queryset -
        # replace this with your own query as appropriate
        all_resources = Image.objects.all()

        paginator = Paginator(all_resources, 24) # Show 5 resources per page

        page = request.GET.get('page')
        try:
            resources = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            resources = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            resources = paginator.page(paginator.num_pages)

        # make the variable 'resources' available on the template
        context = super(ListadoDeImagenes, self).get_context(request)
        context['resources'] = resources

        return context
