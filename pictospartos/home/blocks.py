from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailcore.blocks import (
    CharBlock, ChoiceBlock, ListBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock,
)


class PictoBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    imagen = ImageChooserBlock(required=True, help_text='Selecciona el picto')
    texto = CharBlock(required=False, help_text='Texto que puede acompañar a la imagen')
    #attribucion = CharBlock(required=False)
    descripcion = RichTextBlock(required=False,
        help_text="Notas sobre el uso de la imagen")

    class Meta:
        icon = 'image'
        template = "blocks/picto_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ], blank=True, required=False)

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """
    text = TextBlock()
    attribute_name = CharBlock(
        blank=True, required=False, label='e.g. Mary Berry')

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/blockquote.html"


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="fa-paragraph",
        template="blocks/paragraph_block.html"
    )
    image_block = PictoBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        icon="fa-s15",
        template="blocks/embed_block.html")

class LineaBlock(StreamBlock):
    encabezado = CharBlock(classname="title", required=True, label="Línea de encabezado",
        icon="title")
    pictos = PictoBlock()
    class Meta:
        icon = 'grip'
        #template = "blocks/picto_block.html"

class ContenidoBlock(StreamBlock):
    lineas = LineaBlock()



class Linea2Block(StreamBlock):
    encabezado = CharBlock(classname="title", required=True, label="Línea de encabezado",
        icon="title")
    pictos = ListBlock(PictoBlock())
    class Meta:
        icon = 'grip'
        template = "blocks/fila_pictos.html"


class CarouselBlock(StreamBlock):
    image = ImageChooserBlock()
    

    class Meta:
        icon='cogs'
        template = "blocks/carousel.html"
