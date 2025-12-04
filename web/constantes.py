
# Create your models here.
# Create your models here.
colores = [
    ('', 'Slider texto blanco'),
    ('txt-primary', 'Slider texto blanco texto - azul'),
    ('txt-secondary', 'Slider texto - blanco **'),
    ('txt-tertiary', 'Slider texto - verde'),
    ('txt-quaternary', 'Slider texto - petroleo'),
    ('txt-quinary', 'Slider texto - rosa'),
    ('text-dark', 'Slider texto - negro'),
    ('text-danger', 'Slider texto - rojo'),
    ('text-warning', 'Slider texto - amarillo'),
    ('bg-req-secondary', 'contenido-destacado fondo-amarillo **'),
    ('bg-req-tertiary text-white', 'contenido-destacado fondo-verde'),
    ('bg-req-quaternary text-white', 'contenido-destacado fondo-petroleo'),
    ('bg-req-quinary', 'contenido-destacado fondo-rosa'),
    ('bg-req-primary text-white', 'contenido-destacado texto blanco fondo azul'),
]
COLORES = sorted(colores, key=lambda x: x[1])


tipo_documento = [
    ('sin Calificar', 'Sin Calificar'),
    ('protocolo', 'Protocolo'),
    ('manuel de procedimientos', 'Manual de procedimientos'),
    # (7, ''),
]

COLORES = sorted(colores, key=lambda x: x[1])
TIPO_DOCUMENTO = tipo_documento
# TIPO_DOCUMENTO = sorted(tipo_documento, key=lambda x: x[1])


TIPO_USUARIO = [
    ("","Seleccione un opcion"),
    ("Paciente","Paciente"),
    ("Personal del Hospital","Personal del Hospital"),
    ("Otro","Otro"),
]

TIPO_SUGERENCIA = [
    ("","Seleccione un opcion"),
    ("Denuncia","Denuncia"),
    ("Sugerencia","Sugerencia"),
    ("Agradecimiento","Agradecimiento"),
]



