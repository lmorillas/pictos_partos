# coding: utf-8

import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch, A4, landscape, cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table, Spacer, Frame, PageTemplate, PageBreak
from reportlab.platypus.flowables import HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import (
    black,
    purple,
    white,
    yellow, lightgreen
)
from reportlab.platypus.flowables import Flowable
from functools import partial
import os
BASE_PDF = os.path.dirname(os.path.abspath(__file__)) + '/'



def fuentes():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    reportlab.rl_config.warnOnMissingFontGlyphs = 1
    #pdfmetrics.registerFont(TTFont('Ubuntu', BASE_PDF + 'fonts/Ubuntu-R.ttf' ))
    #pdfmetrics.registerFont(TTFont('UbuntuCon', BASE_PDF + 'fonts/Ubuntu-C.ttf' ))
    pdfmetrics.registerFont(TTFont('Roboto', BASE_PDF + 'fonts/Roboto-Regular.ttf' ))
          


naranja = colors.Color(1, 0.5058823529411764 , 0, 1)
verde = colors.Color(0, 0.7333333333333333, 0.6549019607843137 , 0.7)

class verticalText(Flowable):
    '''Rotates a text in a table cell.'''

    def __init__(self, text):
        Flowable.__init__(self)
        self.text = text

    def draw(self):
        canvas = self.canv
        canvas.rotate(90)
        fs = canvas._fontsize
        canvas.translate(1, -fs/1.2)  # canvas._leading?
        canvas.drawString(0, 0, self.text)

    def wrap(self, aW, aH):
        canv = self.canv
        fn, fs = canv._fontname, canv._fontsize
        return canv._leading, 1 + canv.stringWidth(self.text, fn, fs)

class RotatedPara(Paragraph):
    def draw(self): 
        self.canv.saveState() 
        self.canv.translate(0,0) 
        self.canv.rotate(90) 
        Paragraph.draw(self) 
        self.canv.restoreState()


class Documento(object):
    def __init__(self, orientacion='landscape', fichero='pictos.pdf', compression=None):
        if orientacion == 'landscape':
            _pagesize = pagesize=landscape(A4)
        else:
            _pagesize = A4

        self.src = []
        '''
        self.author = 'Matronas y TCAE del H.U.Miguel Servet. Zaragoza'
        self.subject = 'Pictopartos'
        self.creator = 'https://pictopartos.es'
        self.keywords = ['pictos', 'matronas', 'auxiliares', 'partos', 'arasaac', 'HUMS', 'TCAE']
        '''

        self.doc = SimpleDocTemplate(fichero, pagesize=_pagesize, 
            rightMargin=2*cm,leftMargin=1.5*cm,  topMargin=15 ,bottomMargin=15,
            showBoundary=1, pageCompression=compression)
        # container for the 'Flowable' objects
        #myframe = Frame(self.doc.leftMargin, self.doc.bottomMargin, self.doc.width, self.doc.height, id='framepictos')
        #paginaTemplate = PageTemplate(id='Pagina', frames=[myframe]) #, onPage=self.add_default_info)
        # self.doc.addPageTemplates([paginaTemplate])
        self.elements = [] #[Spacer(1, 0)]
        self.padding_imagenes = 8
        self.get_stylesheet()
        self.alto = 0
        self.ancho = 0
        
        self._max_pictos = 0
        self.max_ancho = self.doc.width - 12
        self.max_alto = self.doc.height - 12

        #self.alto_imagen = self.max_ancho / 8 - self.padding_imagenes * 2
    
    def calc_alto_imagen(self):
        # espacios
        if self.num_lineas > 4:
            self.altura_espacio = 6
        else:
            self.altura_espacio = 12
        max_ancho_imagen = int(self.max_ancho / self.max_cols - self.padding_imagenes * 2)
        max_alto_imagen = int((self.max_alto - self.num_titulos * 28 - \
            (self.num_lineas  - 1)  * self.altura_espacio * 2) / self.num_lineas - 24)
        self.alto_imagen = min(max_ancho_imagen, max_alto_imagen)
        
        

    def contar(self, datos):
        self.num_titulos = sum([1 for x in datos if x.get('titulo')])
        self.num_lineas = sum([1 for x in datos if x.get('linea')])
        lineas = [len(x.get('linea')) for x in datos if x.get('linea')]
        if lineas:
            self.max_cols = max(lineas)
        else:
            self.max_cols = 1

        self.calc_alto_imagen()
  
  

    def get_stylesheet(self):
        self.stylesheet = getSampleStyleSheet()
        self.stylesheet.byName['Normal'].fontName='Roboto'

        self.stylesheet.add(ParagraphStyle(name='titulo', alignment=TA_CENTER, ))
        self.stylesheet.add(ParagraphStyle(name='titulo_imagen', alignment=TA_CENTER, 
        parent = self.stylesheet['Normal'], fontSize=14, fontName='Roboto' ))
        self.stylesheet.add(ParagraphStyle(name="TituloPortada", parent=self.stylesheet['Title'], fontSize=48, leading=52,
        textColor=verde))
        self.stylesheet.add(ParagraphStyle(name="SubtituloPortada", parent=self.stylesheet['Title'], fontSize=24, leading=28,
        textColor=naranja))
        
    
    def parrafo(self, contenido, estilo = None, size='', add=True):
        if size:
            size = 'size={}'.format(size)
        if estilo:
            _estilo = self.stylesheet[estilo]
        else:
            _estilo = self.stylesheet['Normal']
        p = Paragraph('<font {}>{}</font>'.format(size, contenido), 
            style=_estilo)
        ancho, alto = p.wrap(self.doc.width, self.doc.height)
        if add:
            self.alto += alto + p.getSpaceAfter()
            self.elements.append(p)
        else: 
            return p

    def espacio(self, ancho=100, alto = 24 ):
        s = Spacer(ancho, alto)
        ancho, alto = s.wrap(self.doc.width, self.doc.height)
        self.alto += alto
        self.elements.append(s)
    
    def num_titulos(self):
        return len([x for x in self.elements if isinstance(x, Paragraph)])

    def num_filas_pictos(self):
        return len([x for x in self.elements if isinstance(x, Table)])

    def ajustar(self):
        #frame = self.doc.pageTemplate.frames[0]
        #self.max_ancho = self.doc.width - frame._leftPadding - frame._rightPadding
        #self.max_alto = self.doc.height - frame._topPadding - frame._bottomPadding
        self.max_ancho = self.doc.width - 12
        self.max_alto = self.doc.height - 12

        titulos = self.num_titulos()
        lineas = self.num_filas_pictos()
        altura = self.calc_altura()
        
        if altura > max_alto:
            pass
        else:
            pass

    def calc_altura(self):
        total = sum([x.wrap(self.doc.width,self.doc.height)[1] for x in self.elements])
        total += sum(6 for x in self.elements if isinstance(x, Paragraph))
        return total

    def alturas(self):
        print([x.wrap(self.doc.width,self.doc.height)[1] for x in self.elements])

    def anchuras(self):
        print([x.wrap(self.doc.width,self.doc.height)[0] for x in self.elements])

    def imagen_max(self):
        pass        

    def quita_espacios(self):
        self.elements = [e for e in self.elements if not isinstance(e, Spacer)]

    def construir(self): 
        #self.quita_espacios()      
        if self.elements and isinstance(self.elements[-1], Spacer):
            self.elements.pop()
        espacios = [e for e in self.elements if isinstance(e, Spacer)]
        #altura = self.doc.height - self.alto - 24
        #altura = altura/(len(espacios)+1)
        # altura = 3
        altura = self.calc_altura()
        if espacios:
            nespacios = len(espacios)
            alto_espacio = int((self.max_alto - altura ) / nespacios)
            if nespacios < 3 and alto_espacio > 32:
                alto_espacio = int(alto_espacio * 0.7)
            # if self.altura_espacio > alto_espacio:
            self.altura_espacio = alto_espacio

        for e in espacios:
            e.height = self.altura_espacio        
        altura = self.calc_altura()
        if altura < self.max_alto*0.95:
            print('inserto espacio de ', int(self.max_alto-altura)/2)
            self.elements.insert(0, Spacer(1, int(self.max_alto-altura)/2) )
    
    def generar(self):
        self.doc.build(self.elements, onFirstPage=partial(self._vheader,
            titulo=self.titulo,
            logo1=BASE_PDF + "logos/salud.png", logo2=BASE_PDF + "logos/arasaac.png"),
            onLaterPages=partial(self._vheader, titulo=self.titulo, 
            logo1=BASE_PDF + "logos/salud.png", logo2=BASE_PDF + "logos/arasaac.png"))

    def generar_tapa(self):
        self.doc.build(self.elements, onFirstPage=partial(self._tapa,
            logo1=BASE_PDF + "logos/salud.png", logo2=BASE_PDF + "logos/arasaac.png"),
            onLaterPages=partial(self._tapa, titulo=self.titulo, 
            logo1=BASE_PDF + "logos/salud.png", logo2=BASE_PDF + "logos/arasaac.png"))
    
    def linea(self, data):
        wim = data[0][0].drawWidth        
        #print('ancho im -> ', wim, data[0][0].drawHeight )
        # colWidths = [wim + wim*0.4 ] * len(data)        
        colWidths = [wim + self.padding_imagenes * 2 ] * len(data)  # imagen + padding
        #print ('col widths -> ', colWidths)
        t=Table([data], colWidths=colWidths,
        style=[('BOX',(0,0),(-1,-1),0.5, verde), #colors.purple),
           ('ALIGN',(0,0),(-1,-1),'CENTER'),
           ('FONTSIZE', (0,0), (-1,-1), 10),
           #('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
           #('BACKGROUND', (0,0), (-1,-1), colors.lightgrey)
           ('BOTTOMPADDING', (0,0), (-1,-1), 9),
           ('TOPPADDING', (0,0), (-1,-1), 3),
           ('LEFTPADDING', (0,0), (-1,-1), self.padding_imagenes),
           ('RIGHTPADDING', (0,0), (-1,-1), self.padding_imagenes),
        ])
        ancho, alto = t.wrap(self.doc.width, self.doc.height)
        self.alto += alto
        self.ancho = max(ancho, self.ancho)
        if self.elements and not isinstance(self.elements[-1], Paragraph):
            self.espacio(alto=0)
        self.elements.append(t)
        self.espacio(alto=0)
            
        return t
    
    def titulo(self, texto):
        self.parrafo(texto, 'Title')
    
    @staticmethod
    def _vheader(canvas, doc, titulo, logo1=None, logo2=None):
        # Save the state of our canvas so we can draw on it
        #canvas.setStrokeColor(lightgreen)
        canvas.setPageCompression(1)
        #canvas.setStrokeColorCMYK(1, 31, 0, 0)
        #canvas.setStrokeColorRGB(0, 0.7333333333333333, 0.6549019607843137 , 0.7)
        canvas.setStrokeColor(naranja)
        canvas.setLineWidth(1)  
        canvas.saveState()
        canvas.setTitle(titulo)
        canvas.setSubject('Pictopartos')
        canvas.setAuthor('Matronas y TCAE del H.U.Miguel Servet. Zaragoza')		
        canvas.setCreator('https://pictopartos.es')
        canvas.setKeywords(['pictos', 'matronas', 'auxiliares', 'partos', 'arasaac', 'HUMS', 'TCAE'])
        #canvas.translate(0,doc.height) 
        canvas.rotate(-90)
        if logo1:
            #logo_salud = imagen(settings.STATICFILES_DIRS[0]+'/logos/salud.png', 28)
            logo_salud = imagen(logo1, 28)
            logo_salud.drawOn(canvas, -doc.height-doc.topMargin, doc.width + doc.leftMargin + 16 )
        if logo2:
            #logo_arasaac = imagen(settings.STATICFILES_DIRS[0]+'/logos/arasaac.png', 28)
            logo_arasaac = imagen(logo2, 28)
            logo_arasaac.drawOn(canvas, -doc.topMargin - logo_arasaac.drawWidth,
                        doc.width + doc.leftMargin + 16 )
        styles = getSampleStyleSheet()
        header = Paragraph(titulo, styles['Title'])
        header2 = Paragraph('Pictopartos - Matronas y TCAE del HUMS. Pictogramas de @araaac', styles['Italic'])
        w, h = header.wrap(doc.height, doc.leftMargin)
        header.drawOn(canvas, -doc.height-doc.topMargin , doc.width + doc.leftMargin+24) #doc.leftMargin, doc.height + doc.topMargin - h + 12)
        w2, h2 = header2.wrap(doc.height, doc.leftMargin)
        header2.drawOn(canvas, -doc.height-doc.topMargin , doc.width + doc.leftMargin+4) #doc.leftMargin, doc.height + doc.topMargin - h + 12)
        #hr = HRFlowable(width='100%', thickness=0.2, color=colors.purple)
        #hr.wrap( doc.height, doc.topMargin )
        #hr.drawOn(canvas, doc.bottomMargin, -doc.leftMargin )
        canvas.restoreState()

    @staticmethod
    def _tapa(canvas, doc, logo1=None, logo2=None):
        # Save the state of our canvas so we can draw on it
        canvas.setStrokeColor(naranja)
        canvas.setLineWidth(1)  
        canvas.saveState()
        canvas.setSubject('Pictopartos')
        canvas.setAuthor('Matronas y TCAE del H.U.Miguel Servet. Zaragoza')		
        canvas.setCreator('https://pictopartos.es')
        canvas.setKeywords(['pictos', 'matronas', 'auxiliares', 'partos', 'arasaac', 'HUMS', 'TCAE'])
        if logo1:
        #logo_salud = imagen(settings.STATICFILES_DIRS[0]+'/logos/salud.png', 28)
            logo_salud = imagen(logo1, 52)
            logo_salud.drawOn(canvas, doc.leftMargin+4 , doc.height + doc.bottomMargin - logo_salud.drawHeight -4 )
            
        if logo2:
        #logo_arasaac = imagen(settings.STATICFILES_DIRS[0]+'/logos/arasaac.png', 28)
            logo_arasaac = imagen(logo2, 52)
            logo_arasaac.drawOn(canvas, doc.width + doc.leftMargin - logo_arasaac.drawWidth -4, 
                    doc.height + doc.bottomMargin - logo_arasaac.drawHeight- 4)
        canvas.restoreState()

    def _vheaderp(canvas, doc, titulo, logo1=None, logo2=None):
        # Save the state of our canvas so we can draw on it
        canvas.setStrokeColor(verde)
        canvas.setLineWidth(1)  
        canvas.saveState()
        canvas.setTitle(titulo)
        canvas.setSubject('Pictopartos')
        canvas.setAuthor('Matronas y TCAE del H.U.Miguel Servet. Zaragoza')		
        canvas.setCreator('https://pictopartos.es')
        canvas.setKeywords(['pictos', 'matronas', 'auxiliares', 'partos', 'arasaac', 'HUMS', 'TCAE'])
        
        if logo1:
            #logo_salud = imagen(settings.STATICFILES_DIRS[0]+'/logos/salud.png', 28)
            logo_salud = imagen(logo1, 52)
            logo_salud.drawOn(canvas, doc.rightMargin, doc.height )
        if logo2:
            #logo_arasaac = imagen(settings.STATICFILES_DIRS[0]+'/logos/arasaac.png', 28)
            logo_arasaac = imagen(logo2, 52)
            logo_arasaac.drawOn(canvas, doc.width, doc.bottomMargin)
        #canvas.setFont("Courier", 20)
        #canvas.drawCentredString(300, -50, "Encabezado del documento")   
        canvas.restoreState()

    def vertical(self):
        titleFrame_1 = Frame(0.5*inch, 0.75*inch, 7*inch, 9*inch, id='col1', showBoundary=0)
        titleTemplate_1 = PageTemplate(id='OneCol', frames=titleFrame_1)
        document.addPageTemplates([titleTemplate_1])

    def portada(self, titulo=None, subtitulo=None):
        _lineas= []
        _lineas.append(Spacer(1, self.doc.height/2))
        _lineas.append(Paragraph('Título del cuaderno', self.stylesheet['TituloPortada']))
        _lineas.append(Paragraph('subtítulo del cuaderno', self.stylesheet['SubtituloPortada']))
        #_lineas.append(PageBreak())
        self.elements = _lineas #+ self.elements
        
    
def imagen(src, alto=80):   #=1*inch): 
    I = Image(src)
    #I = Image('src/cosa2.png')
    #I.wrap(ancho, alto)
    I.drawWidth = alto * I.drawWidth / I.drawHeight
    I.drawHeight = alto
    return I

def ancho(i):
    return i.drawWidth + 1*cm

def parrafo(estilo, texto='''Texto de la imagen'''):
    P = Paragraph(texto,
        estilo)
    #print ('Parrafo -> ', P.wrap(90,12))
    return P

def crearpdf3x(doc, djson):
    doc.contar(djson)
    
    #doc.ancho_imagen = 85
    for elemento in djson:
        if elemento.get('linea'):
            _datos = []
            pictos = elemento.get('linea')
            for picto in pictos:
                im = picto.get('imagen')
                t = picto.get('texto')
                if im:
                    im = imagen(im, doc.alto_imagen) 
                texto = picto.get('texto', '')
                texto = doc.parrafo(texto, 'titulo_imagen', add=False)
                _datos.append([im, texto])
            doc.linea(_datos)
        if elemento.get('titulo'):
            doc.parrafo(elemento.get('titulo'), 'Title')  

def crearpdf3(doc, djson):    
    for elemento in djson:
        if elemento.get('linea'):
            _datos = []
            pictos = elemento.get('linea')
            for picto in pictos:
                im = picto.get('imagen')
                t = picto.get('texto')
                if im:
                    im = imagen(im, doc.alto_imagen) 
                texto = picto.get('texto', '')
                texto = doc.parrafo(texto, 'titulo_imagen', add=False)
                _datos.append([im, texto])
            doc.linea(_datos)
        if elemento.get('titulo'):
            doc.parrafo(elemento.get('titulo'), 'Title')  
    while doc.calc_altura() > doc.max_alto * 0.97:
        #print(doc.calc_altura(), doc.max_alto)
        #print("Corrigiendo altura", doc.alto_imagen)
        doc.alto_imagen -= int(doc.alto_imagen*0.05)
        #print(doc.alto_imagen)
        doc.elements = []
        crearpdf3(doc, djson)  

def tipos(lista):
    for l in lista:
        h = l.wrap(600,500)[1]
        if isinstance(l, Table):
            print('T', h)
        elif isinstance(l, Spacer):
            print('E', h)
        else:
            print('L', h)

if __name__ == '__main__':

    fuentes()
    import listado

    doc = Documento()
    #doc.parrafo('Pictopartos para la comunicación', 'Title')
    #doc.espacio()
    doc.titulo = "Documento de tests"
    wfilas = {2: 150, 3: 134, 4: 80}
    wwcols = {2: 300, 3: 200, 4: 160, 5: 120}
    datos = listado.cosa0
   
    datos = listado.cosa2l
    doc.contar(datos)
    crearpdf3(doc, datos)
    doc.construir()
    #doc.portada()
    doc.generar()   

    
 