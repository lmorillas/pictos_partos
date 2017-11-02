# coding: utf-8

'''
Creación de cuadernos a partir de las páginas individuales
Gestión de metadatos de los pdf

https://stackoverflow.com/questions/2574676/change-metadata-of-pdf-file-with-pypdf
'''
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import NameObject, createStringObject

BASE_PDF = '/pdf/'
BASE_PDF_TAPA = '/documentos/'

from io import BytesIO

def crea_nombre_pdf(titulo):
    return titulo + 'pdf'

def crea_cuaderno(nombre, listapdf, ruta='', generar=True):
    fins = [PdfFileReader(ruta+'/pdf/' + i+'.pdf') for i in listapdf]
    tapa = PdfFileReader(ruta +'/documentos/' + 'tapa_' + nombre.lower() + '.pdf')
    objetivos = PdfFileReader(ruta +'/documentos/'+'objetivos.pdf')
    observaciones = PdfFileReader(ruta +'/documentos/'+'observaciones.pdf')

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

    fo.addPage(observaciones.getPage(0))
    fo.addPage(observaciones.getPage(0))

    if generar:
        fo.write(open(ruta + 'documentos/Cuaderno ' + nombre + '.pdf', 'wb'))
    else:
        buffer = BytesIO()
        fo.write(buffer)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
        

if __name__ == '__main__':
    from home.models import Cuaderno
    c = Cuaderno.objects.all()[0]
    lista = [n.slug for n in  c.paginadepictos_set.all()]
    crea_cuaderno(c.nombre, lista, ruta=BASE_PDF_TAPA)
