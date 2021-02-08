from django import template
from django.utils.safestring import mark_safe

from mainapp.models import Smartphone


register = template.Library()

TABLE_HEAD = '''
           <table class="table">
             <tbody>
            '''
TABLE_TAIL = '''
             </tbody>
           </table>
             '''
TABLE_CONTENT = '''
           <tr>
             <td>{name}</td>
             <td>{value}</td>
           </tr>
                '''
PRODUCT_SPEC = {
    'notebook': {
        'Cale': 'diagonal',
        'Typ displeja': 'display_type',
        'Czastotnosc procesora': 'processor_freg',
        'RAM' : 'ram',
        'Karta graficzna': 'video',
        'Czas pracy baterii': 'time_without_charge'
    },
    'smartphone': {
        'Cale': 'diagonal',
        'Typ displeja': 'display_type',
        'Rozdzielczosc ekranu': 'resolution',
        'RAM': 'ram',
        'Pojemnosz baterii': 'accum_volume',
        'Dostępność karty SD': 'sd',
        'Objętość pamieci': 'sd_volume_max',
        'Glowna kamera': 'main_cam_mp',
        'Selfi camera': 'frontal_cam_mp'
    }
 }


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Smartphone):
        if not product.sd:
            PRODUCT_SPEC['smartphone'].pop('Максимальный объем SD карты', None)
        else:
            PRODUCT_SPEC['smartphone']['Максимальный объем SD карты'] = 'sd_volume_max'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)

