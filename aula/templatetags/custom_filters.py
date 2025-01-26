from django import template

register = template.Library()

@register.filter
def estado_clase(estado):
    clases = {
        'pendiente': 'bg-secondary',
        'entregado': 'bg-primary',
        'calificada': 'bg-success',
    }
    return clases.get(estado, 'bg-dark')  # 'bg-dark' como valor por defecto
