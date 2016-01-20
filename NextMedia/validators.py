import re
from wtforms import validators
def validatorCorreo(form, field):
    if not re.match('\w+@(\w+)\.com|es',field.data):
        raise validators.ValidationError('Esto no es un correo electronico')

def validatorVISA(form, field):
    if not re.match('(((\d{4}-){3})|((\d{4} ){3}))\d{4}',field.data):
        raise validators.ValidationError('Esto no es una Tarjeta de credito')

def validatorApellidos(form,field):
    if not re.match('\w+ \w+',field.data):
        raise validators.ValidationError('No has puesto tus apellidos')
