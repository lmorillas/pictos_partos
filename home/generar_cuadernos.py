from utils import Documento, fuentes

import yaml
#from home.models import Cuaderno

subtitulo = 'Matronas y TCAE del H.U. Miguel Servet. Zaragoza.'

cuadernos = '''Urgencias
Planta Sexta (Fisiopatología fetal)
Dilatación - Paritorio
Plantas de Puerperio (Quinta y Séptima)'''

cuadernos='''
Urgencias:
    - Alicia Larraz Miguel
    - Eva Pascual Collados
    - Carmen Sánchez Castaño
    - Laura Saz Simón
    - Mª Jesús Solanas Sancho
Fisiopatología fetal (Planta sexta):
    - Julia Berdún Pueyo
    - Noelia Buil Carrera
    - Irene Campos Trol
    - Juan  Izquierdo Villarroya
    - M. Rosario Laencina Lázaro
    - Esther Monserrat Cantera
    - Nelia Villuendas Fernández
Dilatación - Paritorio:
    - Marta Arnal García
    - Lourdes García-Lisbona Iriarte
    - Sofía Martínez Carballo
    - Mª Jesús Royo Viñado
    - Isabel Sebastián Gurría
Puerperio (Plantas Quinta y Séptima):
    - Rebeca Amayas Lorao
    - Ana Belén Laviña Castán
    - Cristina Oliván Lambea
    - Carmen Serrano Ibáñez
    - Esther Viñerta Serrano
'''

fuentes()

listacuadernos = yaml.load(cuadernos)

for c in listacuadernos:
    doc = Documento(fichero=c.lower()+ '.pdf')
    doc.portada(c, subtitulo, participantes=listacuadernos.get(c))
    doc.generar_tapa()


