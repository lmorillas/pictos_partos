# coding: utf-8

'''
Creación de cuadernos a partir de las páginas individuales
Gestión de metadatos de los pdf

https://stackoverflow.com/questions/2574676/change-metadata-of-pdf-file-with-pypdf
'''
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import NameObject, createStringObject

BASE_PDF = 'pdfs/'
BASE_PDF_TAPA = 'pdfs/'
DESTINO_CUADERNO= ''

def crea_nombre_pdf(titulo):
    return titulo + 'pdf'

def crea_cuaderno(nombre, tapa, listapdf):
    fins = [PdfFileReader(BASE_PDF+i) for i in listapdf]
    tapa = PdfFileReader(BASE_PDF + 'tapa_' + nombre.lower() + '.pdf')
    objetivos = PdfFileReader(BASE_PDF+'objetivos.pdf')

    # gestión metadatos
    info_old = fins[0].getDocumentInfo()
    output = crea_nombre_pdf(nombre)
    fo = PdfFileWriter()
    info_dict = fo._info.getObject()
    
    for key in info_old:
        info_dict.update({NameObject(key): createStringObject(info_old[key])})
    info_dict.update({
        NameObject('/Title'): createStringObject(nombre)
    })

    # crear con páginas
    # añadir tapa fo.addPage()
    # añadir objetivos
    
    fo.addPage(tapa.getPage(0))
    fo.addPage(objetivos.getPage(0))

    for i in fins:
        fo.addPage(i.getPage(0))

    fo.write(open(DESTINO_CUADERNO  +  'Cuaderno ' + nombre + '.pdf', 'wb'))

if __name__ == '__main__':
    from home.models import Cuaderno
    c = Cuaderno.objects.all()[0]
    lista = [n.slug+'.pdf' for n in  c.paginadepictos_set.all()]
    crea_cuaderno(c.nombre, 'objetivos.pdf', lista)
