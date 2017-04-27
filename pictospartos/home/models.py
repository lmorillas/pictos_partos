# coding: utf-8

from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, 
    StreamFieldPanel,
)

from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.wagtailimages.models import Image

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Orderable, ClusterableModel

from wagtail.wagtailimages.models import Image

from wagtail.wagtailcore.blocks import (
    CharBlock, ChoiceBlock, ListBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock,
)

from .blocks import LineaBlock,ContenidoBlock, Linea2Block, CarouselBlock





class HomePage(Page):
    carousel = StreamField(CarouselBlock(), null=True, blank=True)
    content_panels = Page.content_panels + [
        StreamFieldPanel('carousel'),
    ]



class PaginaPictos(Page):
    subtitulo = models.CharField("Subtítulo de la página", max_length=254, blank=True, 
        help_text="Texto que puede aparecer debajo del título de la página")
    lineas1 = StreamField(LineaBlock(), blank=True, verbose_name="Líneas")

    content_panels = Page.content_panels + [
        FieldPanel('subtitulo', classname="full"),
        StreamFieldPanel('lineas1'),
    ]

class Pagina2Pictos(Page):
    subtitulo = models.CharField("Subtítulo de la página", max_length=254, blank=True, 
        help_text="Texto que puede aparecer debajo del título de la página")
    lineas = StreamField(ContenidoBlock(), blank=True, verbose_name="Líneas")

    content_panels = Page.content_panels + [
        FieldPanel('subtitulo', classname="full"),
        StreamFieldPanel('lineas'),
    ]


class Pagina3Pictos(Page):
    subtitulo = models.CharField("Subtítulo de la página", max_length=254, blank=True, 
        help_text="Texto que puede aparecer debajo del título de la página")
    #lineas = ListBlock StreamField(Linea2Block(), blank=True, verbose_name="Líneas")

    contenido = StreamField(Linea2Block(), null=True,blank=True,
        help_text="Líneas de pictos que aparecen en la página",
        verbose_name="Líneas de pictos",)
    
    content_panels = Page.content_panels + [
        FieldPanel('subtitulo', classname="full"),
        StreamFieldPanel('contenido'),
    ]

'''
class Linea(Page):
    page = ParentalKey(PaginaPictos, related_name='linea_pictos')
    titulo = models.CharField("Título bloque", max_length=254, blank=True)

    content_panels = [
        FieldPanel('titulo', classname="full"),
        InlinePanel('picto_relacionado', label="Picto"),
    ]

class Pictograma(models.Model):
    """

    """
    page = ParentalKey(Linea, related_name='picto_relacionado')
    nombre = models.CharField("Nombre del picto", max_length=64, blank=True)
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

    panels = [
        FieldPanel('nombre', classname="full"),
        ImageChooserPanel('picto'),
        FieldPanel('descripcion'),
    ]
'''

'''
class Pagina(Page):
	titulo = models.CharField("Título de la página", max_length=254, blank=True)
	
'''

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





