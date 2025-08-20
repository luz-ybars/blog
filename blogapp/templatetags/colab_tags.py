from django import template

register = template.Library()

@register.filter
def es_colaborador(user):
    try:
        return user.is_authenticated and (getattr(user, 'is_superuser', False) or user.groups.filter(name='Colaborador').exists())
    except Exception:
        return False
