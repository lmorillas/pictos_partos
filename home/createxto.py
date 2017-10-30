# coding: utf-8

from utils import Documento, fuentes
import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch, A4, landscape, cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table, Spacer, Frame, PageTemplate, PageBreak, FrameBreak
from reportlab.platypus.flowables import HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus.doctemplate import BaseDocTemplate

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


fuentes()
texto = '''El <b>Hospital Universitario Miguel Servet</b> (HUMS) es el centro sanitario de referencia para una población cada vez más heterogénea en cuanto a cultura, necesidades, idioma, religión,… este enriquecimiento cultural trae consigo un gran obstáculo en el día a día de la jornada laboral, que dificulta el correcto desarrollo de la atención sanitaria: la barrera idiomática.
Una adecuada comunicación con cada paciente de forma bidireccional (pacientes-profesionales; profesionales-pacientes) es imprescindible para poder garantizar una atención integral e integrada en cada momento del proceso de salud.
El parto es un acontecimiento de gran importancia en la vida de una mujer y de una familia que exige el compromiso del equipo sanitario para ofrecer la información pertinente y adecuada en cada momento.
La comunicación entre la madre y el equipo que la atiende  (matrona, TCAE y tocólogo) es una parte esencial en el cuidado.
No sólo se pretende que  las pacientes entiendan lo que el personal sanitario quiere transmitir. Es indispensable que los profesionales comprendan lo que la paciente puede necesitar y lo que quiera comunicar al equipo sanitario. 
Para que todo esto pueda llevarse a cabo, se utilizará como herramienta de comunicación un método alternativo al lenguaje oral: comunicación aumentativa, en forma de pictogramas. 
Será también útil en la atención a las mujeres con problemas cognitivos, o de audición, cuando lleguen a nuestro servicio. 
Este cuaderno tiene como objetivo eliminar las dificultades de comunicación entre la paciente y su acompañante con el equipo sanitario a lo largo de todo el ingreso en el servicio de dilatación del HUMS, aumentando el confort y la seguridad en el parto. 
Está formado por láminas con pictogramas. Cada cuaderno tiene una estructura diferente, según las necesidades que vemos los profesionales en cada parte del Servicio de Obstetricia.

<i>Servicio de Obstetricia H.U.M.S. 2017 (Versión 0.1)</i>'''

condiciones = '''Los pictogramas de <b>arasaac</b> (ver <u><a href=http://blog.arasaac.org/p/condiciones-de-uso_19.html>http://blog.arasaac.org/p/condiciones-de-uso_19.html</a></u>) son propiedad del Gobierno de Aragón (España).
 Sus recursos se publican bajo Licencia Creative Commons (BY-NC-SA).'''

materiales = '''Nuestros materiales, como <b>Proyecto de Mejora de la Calidad del H.U.M.S</b>, están
a disposición del personal sanitario que los quiera utilizar o mejorar, siempre que se cite su procedencia.'''

beta= '''Estos materiales están en fase de prueba y en ningún caso garantizan la perfecta comunicación entre la paciente y el personal sanitario. 
Es éste el que tiene que valorar la validez de la comunicación.'''

destino = 'pdfs/'
doc = Documento(fichero= destino + 'objetivos.pdf')
doc.titulo = 'Cuadernos para la comunicación'
estilo_texto = doc.stylesheet['Normal']
estilo_texto.spaceAfter = 6
doc.pagina_de_texto(texto)
doc.elements.append(FrameBreak())
doc.elements.append(Paragraph('Condiciones de uso', style=doc.stylesheet['Heading2']))
doc.elements.append(Paragraph(condiciones, style=estilo_texto))
doc.elements.append(Paragraph(materiales, style=estilo_texto))
doc.elements.append(Paragraph('Limitación de responsabilidad', style=doc.stylesheet['Heading2']))
doc.elements.append(Paragraph(beta, style=estilo_texto))

doc.generarwm('Servicio de Obstetricia. HUMS')


