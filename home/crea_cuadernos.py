# coding: utf-8

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import NameObject, createStringObject

BASE_PDF = 'pdfs/'

def crea_nombre_pdf(titulo):
    return titulo + 'pdf'

def crea_cuaderno(nombre, tapa, listapdf):
    fins = [PdfFileReader(BASE_PDF+i) for i in listapdf]
    tapa = PdfFileReader(BASE_PDF+tapa)

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
    for i in fins:
        fo.addPage(i.getPage(0))
    fo.write(open('cosa.pdf', 'wb'))
