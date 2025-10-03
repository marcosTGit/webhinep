
# Create your models here.
# Create your models here.
colores = [
    ('', 'sin color'),
    ('txt-primary', 'texto blanco texto - azul'),
    ('txt-secondary', 'texto - blanco'),
    ('txt-tertiary', 'texto - verde'),
    ('txt-quaternary', 'texto - petroleo'),
    ('txt-quinary', 'texto - rosa'),
    ('text-dark', 'texto - negro'),
    ('text-danger', 'texto - rojo'),
    ('text-warning', 'texto - amarillo'),
    ('bg-req-secondary', 'fondo-amarillo'),
    ('bg-req-tertiary text-white', 'fondo-verde'),
    ('bg-req-quaternary text-white', 'fondo-petroleo'),
    ('bg-req-quinary', 'fondo-rosa'),
    ('bg-req-primary text-white', '* texto blanco fondo azul'),
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



