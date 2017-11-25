from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from wagtail.wagtailcore import hooks

from .models import PaginaDePictos
from .models import generar_pdf
from .crea_cuadernos import crea_cuaderno
from django.conf import settings

ruta_pdf = settings.STATIC_ROOT + '/pdf/'
ruta_doc = settings.STATIC_ROOT + '/documentos/'

@hooks.register('after_create_page')
@hooks.register('after_edit_page')
def do_after_edit_page(request, page):
    # Use a custom create view for the AwesomePage model
    
    if isinstance (page, PaginaDePictos):
        #print('Creando ... {}{}.pdf'.format(ruta_pdf, page.slug))
        open('{}{}.pdf'.format(ruta_pdf, page.slug), 'wb').write(generar_pdf(page))
        for c in page.cuaderno.all():
            listapdf = [n.slug for n in  c.paginadepictos_set.all().order_by('title')]
            doc = crea_cuaderno(c.nombre, listapdf, ruta = settings.STATIC_ROOT , generar=False)
            open('{}Cuaderno {}.pdf'.format(ruta_doc, c.nombre), 'wb').write(doc)



'''
N.B. To see what icons are available for use in Wagtail menus and StreamField block types,
enable the styleguide in settings:

INSTALLED_APPS = (
   ...
   'wagtail.contrib.wagtailstyleguide',
   ...
)

or see http://kave.github.io/general/2015/12/06/wagtail-streamfield-icons.html

This demo project includes the full font-awesome set via CDN in base.html, so the entire
font-awesome icon set is available to you. Options are at http://fontawesome.io/icons/.
'''

