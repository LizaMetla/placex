from django import template

register = template.Library()


@register.filter()
def set_error_false(request):
    request.session['is_error'] = False
    request.session.save()
    return ''
