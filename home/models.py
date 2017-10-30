# coding: utf-8

from __future__ import absolute_import, unicode_literals

from django.db import models
from django.http import HttpResponse

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

from .blocks import CarouselBlock, BaseStreamBlock
from wagtail.wagtailsnippets.models import register_snippet
from modelcluster.fields import ParentalManyToManyField

from django import forms


from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailcore.blocks import (
    CharBlock, ChoiceBlock, ListBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock,
)
from wagtail.wagtailsearch import index

class HomePage(Page):
    carousel = StreamField(CarouselBlock(), null=True, blank=True)

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)

        # Add extra variables and return the updated context
        context['cuadernos'] = Cuaderno.objects.all().order_by('nombre')
        context['paginas'] = PaginaDePictos.objects.live().order_by('title')
        return context
    content_panels = Page.content_panels + [
        StreamFieldPanel('carousel'),
    ]



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




@register_snippet
class Cuaderno(models.Model):
    """
    Standard Django model that is displayed as a snippet within the admin due
    to the `@register_snippet` decorator. We use a new piece of functionality
    available to Wagtail called the ParentalManyToManyField on the BreadPage
    model to display this. The Wagtail Docs give a slightly more detailed example
    http://docs.wagtail.io/en/latest/getting_started/tutorial.html#categories
    """
    nombre = models.CharField(max_length=255)

    panels = [
        FieldPanel('nombre'),
    ]

    def __str__(self):
        return self.nombre
    def paginas(self):
        return self.paginadepictos_set.live().order_by('title')

    class Meta:
        verbose_name_plural = 'Cuadernos'

from io import BytesIO
from .utils import Documento, fuentes, parrafo, imagen, crearpdf3
from django.conf import settings
ruta_imagen = settings.STATICFILES_DIRS[0] + '/images/'
ruta_pdf = settings.STATICFILES_DIRS[0] + '/pdf/'


def crea_linea(linea):
    _datos = []
    for bloque in linea:
        bl = {}
        im = bloque.imagen
        if im:
            bl['imagen'] =  bloque.imagen.file.path
        else:
            bl['imagen']= ruta_imagen + 'noimagen.png'
        texto = bloque.texto
        if texto:
            bl['texto'] = texto
        else:
            bl['texto'] = ''
        _datos.append(bl)
    #print(_datos)
    return _datos

def limpia_punto(cadena):
    cadena = cadena.strip()
    if cadena.endswith('.'):
        return cadena[:-1]
    else:
        return cadena

def generar_cuaderno(hoja):
    pass

def generar_pdf(hoja):
    buffer = BytesIO()
    fuentes()
    doc = Documento(fichero=buffer, compression=1)
    doc.titulo = limpia_punto(hoja.title)
    
    linea1 = hoja.linea1.all()
    linea2 = hoja.linea2.all()
    linea3 = hoja.linea3.all()
    linea4 = hoja.linea4.all()

    datos = []
    if hoja.tit1:
        datos.append({'titulo': hoja.tit1})
    if linea1:
        fila = crea_linea(linea1)
        if fila:
            datos.append({'linea': fila})
    if hoja.tit2:
        datos.append({'titulo': hoja.tit2})
    if linea2:
        fila = crea_linea(linea2)
        if fila:
            datos.append({'linea': fila})
    if hoja.tit3:
            datos.append({'titulo': hoja.tit3})
    if linea3:
        fila = crea_linea(linea3)
        if fila:
            datos.append({'linea': fila})
    if hoja.tit4:
        datos.append({'titulo': hoja.tit4})
    if linea4:
        fila = crea_linea(linea4)
        if fila:
            datos.append({'linea': fila})

    doc.contar(datos)
    crearpdf3(doc, datos)

    doc.construir()
    doc.generar()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf

class PaginaCuadernos(Page):
    pass

class PaginaDePictos(Page):
    cuaderno = ParentalManyToManyField('Cuaderno', blank=True,
        help_text="Selecciona el cuaderno o cuadernos en que debe de aparecer")
    subtitulo = models.CharField("Subtítulo de la página", max_length=254, blank=True, 
        help_text="Texto que puede aparecer debajo del título de la página")
    tit1 = models.CharField("Título de la línea", max_length=254, blank=True)
    tit2 = models.CharField("Título de la línea", max_length=254, blank=True)
    tit3 = models.CharField("Título de la línea", max_length=254, blank=True)
    tit4 = models.CharField("Título de la línea", max_length=254, blank=True)
    observaciones = RichTextField(blank=True)
    generarpdf = models.BooleanField("Generar pdf", default=True)

    '''
    def serve(self, request):
        if "format" in request.GET:
            if request.GET['format'] == 'pdf':
                if self.generarpdf:
                    open('{}{}.pdf'.format(ruta_pdf, self.slug), 'wb').write(generar_pdf(self))
                    self.generarpdf = False
                    self.save()
                

                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(self.slug)
                response.write(pdf)
                return response
            else:
                # Unrecognised format error
                message = 'No podemos exportar en este formato: ' + request.GET['format']
                return HttpResponse(message, content_type='text/plain')
        else:
            # Display event page as usual
            return super(PaginaDePictos, self).serve(request)
    '''

    search_fields = Page.search_fields + [ # Inherit search_fields from Page
        index.RelatedFields('linea1', [
            index.SearchField('tit1'),
            index.SearchField('imagen'),
            index.SearchField('texto')])
    ]

    content_panels = Page.content_panels + [
        FieldPanel('generarpdf'),
        FieldRowPanel([FieldPanel('cuaderno', widget=forms.CheckboxSelectMultiple,
            classname="col5"), 
            FieldPanel('subtitulo', classname="col7")],
            ),
        MultiFieldPanel([
            FieldPanel('tit1'),
            InlinePanel('linea1', label="Pictos"),
        ],
        heading="Primera fila de pictos",
        classname="collapsible collapsed",
        ),
        MultiFieldPanel([
            FieldPanel('tit2'),
            InlinePanel('linea2', label="Pictos"),
        ],
        heading="Segunda fila de pictos",
        classname="collapsible collapsed",
        ),
        MultiFieldPanel([
            FieldPanel('tit3'),
            InlinePanel('linea3', label="Pictos"),
        ],
        heading="Tercera fila de pictos",
        classname="collapsible collapsed",
        ),
        MultiFieldPanel([
            FieldPanel('tit4'),
            InlinePanel('linea4', label="Pictos"),
        ],
        heading="Cuarta fila de pictos",
        classname="collapsible collapsed",
        ),
        FieldPanel('observaciones'),
        ]


class PictoBlock(Orderable):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    linea1 = ParentalKey(PaginaDePictos, related_name="linea1", blank=True, null=True)
    linea2 = ParentalKey(PaginaDePictos, related_name="linea2", blank=True, null=True)
    linea3 = ParentalKey(PaginaDePictos, related_name="linea3", blank=True, null=True)
    linea4 = ParentalKey(PaginaDePictos, related_name="linea4", blank=True, null=True)

    imagen = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    texto = models.CharField(max_length=120,  help_text='Texto que puede acompañar a la imagen',blank=True)

    panels = [
        
            ImageChooserPanel('imagen'),
            FieldPanel('texto'),
        ]



class PaginaEstandar(Page):
    """
    A generic content page. On this demo site we use it for an about page but
    it could be used for any type of page content that only needs a title,
    image, introduction and body field
    """

    introduction = models.TextField(
        verbose_name = 'Introducción',
        help_text='Texto para describir la página',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name = 'Imagen',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Sólo en modo horizontal. anchura entre 1000px y 3000px.'
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Cuerpo de la página", blank=True
    )
    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        StreamFieldPanel('body'),
        ImageChooserPanel('image'),
    ]